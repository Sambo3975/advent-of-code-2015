import warnings


class CircuitComputer:
    """A circuit computer that processes a language somewhat like Verilog"""

    def __init__(self):
        self.__open_file = ''
        self.__open_file_lines = None
        self.__line_number = None
        self.__instructions = None
        self.__wires = None
        self.__has_computed_wires = False
        self.__binaries = {
            'AND': lambda x, y: x & y,
            'OR': lambda x, y: x | y,
            'LSHIFT': lambda x, y: x << y,
            'RSHIFT': lambda x, y: x >> y,
        }
        self.__unaries = {
            'NOT': lambda x: ~ x,
        }

    def __repr__(self):
        string = 'CircuitComputer'
        if self.__wires is not None and len(self.__wires) > 0:
            string += ' with wire signals:'
            # Sort using a very lazily-written lexicographic ordering
            for key in sorted(self.__wires, key=lambda identifier: (len(identifier) - 1) * 1000 + ord(identifier[-1])):
                string += f"\n  {key}: {self.__wires[key]}"
        else:
            string += ', has no wire signals'
        return string

    # File loading

    def __parse_symbol(self, symbol):
        try:  # If this works, we have a wire signal
            symbol = int(symbol)
            if symbol >> 16 != 0:
                self.__warn(f'Attempt to set a wire signal to a value wider than 16 bits (unsigned): {symbol}. Value '
                            f'will be truncated to {symbol & 0xffff}.')
            return symbol
        except ValueError:  # If not, we have either an operator or a wire identifier
            if symbol in self.__unaries:
                return self.__unaries[symbol]
            if symbol in self.__binaries:
                return self.__binaries[symbol]
            self.__check_wire_identifier(symbol)
            return symbol

    def parse_file(self, file_name):
        if file_name != self.__open_file:
            with open(file_name) as f:
                self.__open_file_lines = f.readlines()

        self.__open_file = file_name
        self.__wires = {}

        split_lines = [x.split() for x in self.__open_file_lines]
        for i in range(len(split_lines)):
            self.__line_number = i + 1
            line = split_lines[i]
            wire = line[-1]
            # Parse the symbols in the line
            parsed_symbols = [self.__parse_symbol(symbol) for symbol in line[:-2]]  # Don't parse the '-> wire' part
            # Ensure that the operator is always last
            if len(parsed_symbols) > 1:
                parsed_symbols[-2], parsed_symbols[-1] = parsed_symbols[-1], parsed_symbols[-2]
            self.__wires[wire] = parsed_symbols

        self.__has_computed_wires = False
        self.__line_number = None

    # Checks

    def __check_wire_identifier(self, wire):
        if not wire.islower():
            self.__error(f"Invalid wire identifier: '{wire}'")

    def __error(self, message):
        if self.__line_number is not None:
            raise RuntimeError(f"{self.__open_file} line {self.__line_number}: {message}")
        else:
            raise RuntimeError(message)

    def __warn(self, message):
        if self.__line_number is not None:
            warnings.warn(f"{self.__open_file} line {self.__line_number}: {message}")
        else:
            warnings.warn(message)

    # Getters

    def get_wire_signal(self, wire, visited=None):
        """
        Get the signal on the given wire. Only computes the signals upon which the given wire depends. To compute all
        signals, call get_all_wire_signals.
        """
        self.__has_computed_wires = True
        # make sure we are checking a wire that exists
        if wire not in self.__wires:
            self.__error(f"Wire '{wire}' is undefined")
        # Circular dependency detection and handling
        if visited is None:
            visited = []
        elif wire in visited:
            index = visited.index(wire)
            error_message = f"Circuit contains a circular dependency between wires {visited[index]}"
            for i in range(index + 1, len(visited)):
                error_message += f", {visited[i]}"
            self.__error(error_message + f", {wire}")
        visited.append(wire)

        signal = self.__wires[wire]
        if isinstance(signal, int):
            visited.pop(-1)
            return signal
        for i in range(len(signal)):
            symbol = signal[i]
            if not isinstance(symbol, int):  # If the symbol is an integer, do nothing
                if isinstance(symbol, str):  # If it is a string, it is a wire identifier. Get the signal on that wire.
                    signal[i] = self.get_wire_signal(symbol, visited)
                else:  # It is a function. We can assume it is the last element. Call it on the other elements.
                    func = signal[-1]
                    if len(signal) == 2:  # 1 parameter
                        self.__set_wire_signal_raw(wire, func(signal[0]))
                    else:  # 2 parameters
                        self.__set_wire_signal_raw(wire, func(signal[0], signal[1]))
                    visited.pop(-1)
                    return self.__wires[wire]
        self.__set_wire_signal_raw(wire, signal[0])
        visited.pop(-1)
        return self.__wires[wire]

    def get_all_wire_signals(self):
        """Get the signal values of all wires, computing any that have not yet been computed."""
        if self.__wires is None:
            self.__error('Circuit file not loaded.')
        # No wire selected. Get the signal on all of them.
        for key in self.__wires:
            self.get_wire_signal(key)
        return self.__wires

    def get_all_wire_signals_raw(self):
        """Get the signal values of all wires, NOT computing any that have not yet been computed"""
        if self.__wires is None:
            self.__error('Circuit file not loaded.')
        return self.__wires

    def __set_wire_signal_raw(self, wire, value):
        """Set a wire's signal WITHOUT propagating the effect of the change. For internal use only."""
        self.__check_wire_identifier(wire)
        if isinstance(value, int):
            self.__wires[wire] = value & 0xffff  # Restrict to 16-bit values
        else:
            self.__error(f"Cannot assign a signal to {value}.")

    def set_wire_signal(self, wire, value):
        """Set a wire's signal. Resets the wires dict."""
        if self.__has_computed_wires:
            self.parse_file(self.__open_file)
        self.__set_wire_signal_raw(wire, value)


def test0():
    # No file loaded
    # Should cause RuntimeError
    computer = CircuitComputer()
    computer.get_all_wire_signals()


def test1():
    expected_signals = {
        'd': 72,
        'e': 507,
        'f': 492,
        'g': 114,
        'h': 65412,
        'i': 65079,
        'x': 123,
        'y': 456,
    }
    for wire in expected_signals:
        computer = CircuitComputer()
        computer.parse_file('test1.txt')
        computer.get_wire_signal(wire)
        result = computer.get_all_wire_signals_raw()
        for key in result:
            if not (isinstance(result[key], list) or result[key] == expected_signals[key]):
                print(f"  FAIL for wire {wire}. Expected: wire '{key}' == {expected_signals[key]}"
                      f"                        Actual:   wire '{key}' == {result[key]}")


def test2():
    print("Test 2. Circular Dependency")
    computer = CircuitComputer()
    computer.parse_file('test2.txt')
    computer.get_wire_signal('a')


if __name__ == '__main__':
    circuit_computer = CircuitComputer()
    circuit_computer.parse_file('input.txt')
    signal_value = circuit_computer.get_wire_signal('a')
    print(f"Before overriding 'b' to 'a': Wire 'a' has signal {signal_value}")
    circuit_computer.set_wire_signal('b', signal_value)
    signal_value = circuit_computer.get_wire_signal('a')
    print(f"After overriding 'b' to 'a': Wire 'a' has signal {signal_value}")

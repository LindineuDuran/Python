def int_to_roman(input):
    if not isinstance(input, int):
        raise TypeError("expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []

    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def roman_to_int(input):
    if not isinstance(input, str):
        raise TypeError("expected string, got %s" % type(input))
    input = input.upper()
    nums = {'M':1000,
            'D':500,
            'C':100,
            'L':50,
            'X':10,
            'V':5,
            'I':1}
    total = 0
    last_value = 0
    
    for char in input:
        value = nums.get(char, 0)
        if value > last_value:
            total += value - 2 * last_value
        else:
            total += value
        last_value = value
        
    if int_to_roman(total) == input:
        return total
    else:
        raise ValueError('input is not a valid Roman numeral: %s' % input)

print(roman_to_int('XVI'))  # Output: 16

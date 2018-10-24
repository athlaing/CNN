function binaryToDecimal(binary:: String, signed:: Bool)
    sum = 0
    index = length(binary)
    for i in binary
        if (signed && index == length(binary))
            if i == '1'
                sum += -1 * 2 ^ (index - 1)
            end
            index -= 1
            continue
        else
            if i == '1'
                sum += 2 ^ (index - 1)
            end
        end
        index -= 1
    end
    return sum
end

unsignedToDecimal(binary:: String) = binaryToDecimal(binary, false);

signedToDecimal(binary:: String) = binaryToDecimal(binary, true);

function Bfloat16ToDecimal(float:: String)
  sign = 1
  exp = 0
  man = Array{Char,1}(undef,8)
  for i = 1:16
    if i == 1 && float[i] == '1'
      sign = -1
    elseif i <= 9 && i >= 2
      if float[i] == '1'
        exp += 2.0 ^ (9 - i)
      end
    elseif i <= 16 && i >= 10
      man[17-i] = float[i]
    end
  end
  man[8] = '1'
  for bit in man
    if bit == '1' && exp == 0
      man[8] = '0'
      break
    end
  end
  mantissa = 0
  for i = 1:8
    if man[i] == '1'
      mantissa += 2.0 ^ (i - 8)
    end
  end
  if exp == 0
    if !checkSignificand
      return 0.0
    else
      return sign * 2.0 ^ (-126) * mantissa
    end
  elseif exp == 255
    return error("Inf or NaN")
  else
    return sign * 2.0 ^ (exp - 127) * mantissa
  end
end

function decimalToBfloat16(num::Float64)
  if num == 0
    return "0000000000000000"
  end
  if num < 0
    sign = '1'
    num *= -1
  else
    sign = '0'
  end
  decimal = num - floor(num)
  result = decimalToUnsigned(Int(floor(num)))
  intLength = length(result)
  if(result == "")
    lessThanZero = true
    n = 8
  else
    lessThanZero = false
    n = 8 - intLength
  end
  manResult = Array{Char,1}()
  firstBit = true
  zeroCounter = 0
  while(n > 0)
    decimal *= 2
    if firstBit && lessThanZero
      if decimal >= 1
        decimal -= 1
        push!(manResult, '1')
        n -= 1
        firstBit = false
      end
      zeroCounter += 1
    else
      if decimal >= 1
        decimal -= 1
        push!(manResult, '1')
      else
        push!(manResult, '0')
      end
      n -= 1
    end
  end
  for i in manResult
    result *= i
  end
  if zeroCounter == 0
    exp = intLength + 126
  else
    exp = -1 * zeroCounter + 127
  end
  expResult = decimalToUnsigned(exp)
  padZeros = 8 - length(expResult)
  for i = 1 : padZeros
    expResult = '0' * expResult
  end
  return sign * expResult * result[2:8]
end

function decimalToUnsigned(num:: Int64)
  unsigned = Array{Char,1}()
  result = ""
  if(num == 0)
    return result
  elseif (num < 0)
    error("Input must be >= 0")
  end
  while(num != 1)
    if !Bool(num % 2)
      push!(unsigned, '0')
    else
      push!(unsigned, '1')
    end
    num = div(num, 2)
  end
  if(num == 1)
    push!(unsigned, '1')
  else
    push!(unsigned, '0')
  end
  for i = length(unsigned):-1:1
    result *= unsigned[i]
  end
  return result
end

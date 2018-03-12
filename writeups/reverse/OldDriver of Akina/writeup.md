# 秋名山老司机
这个题目的本质是一个比较理想化的压缩算法。称为算术编码。这个算法最大的特征就是将输入的二进制序列映射到了实数轴上的[0,1)之间的一个区间。当然，数据越多，这个区间也就越小。相对应的，这个数字的精度越高。

具体的编码方式可以参考下面的论文：
https://wenku.baidu.com/view/af2e25ab6f1aff00bed51ea9.html

由于bmp有RGB三个色道。这次的算法将三个色道分别压缩，以提高压缩效果。

这里对符号概率Q的推算使用的bmp当前像素点左上的4*4个像素点中01的统计得出。然后直接近似的出Q的值。默认情况下以1位符号概率较大者。当然，这个若0出现概率大于1，可以直接对调H和L相应的值。对压缩没有影响，且解码时也可以根据之前值重新推测符号概率。

# OldDriver of Akina

This time, I use a compression algorithm called arithmetic coding. The biggest feature of this algorithm is that it mapping the input binary sequence to an interval on the real axis.

Here is the decode code
```python
def get_bit(data):
    last = data[-2:]
    data = data[:-2]
    for ch in data:
        for i in range(8):
            yield ch & 1
            ch >>= 1
    ch = last[0]
    for i in range(last[1]):
        yield ch & 1
        ch >>= 1


def decode(bit_yield):
    buffer = bytearray(1024 * 1024 * 3)
    bit_num = []
    for i in range(0x100):
        one = 0
        for j in range(8):
            if i & 1:
                one += 1
            i >>= 1
        bit_num.append(one)
    q_list = [7, 7, 6, 5, 5, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    CS = 0
    for i in range(8):
        bit = next(bit_yield)
        CS <<= 1
        CS += bit

    AS = 0xff
    try:
        for rgb in range(3):
            for i in range(1024):
                print(i)
                for j in range(1024):
                    byte = 0
                    sum1 = 0
                    for x in range(4):
                        for y in range(4):
                            if x == 0 and y == 0:
                                continue
                            if i - x < 0 or j - y < 0:
                                ch = 0xff
                            else:
                                # if i > 475:
                                #     print(x,y,i,j)
                                #     print((1024 * (i - x) + (j - y)) * 3 + rgb)
                                ch = buffer[(1024 * (i - x) + (j - y)) * 3 + rgb]
                            sum1 += bit_num[ch]
                    if sum1 < 60:
                        H = 0
                        Q = q_list[sum1]
                    else:
                        H = 1
                        Q = q_list[120 - sum1]
                    for n in range(8):
                        AL = AS >> Q
                        AH = AS - AL

                        if CS < AH:
                            byte += (H << n)
                            AS = AH
                        else:
                            byte += (0 if H else 1) << n
                            CS = CS - AH
                            AS = AL

                        while AS & 0x80 == 0:
                            AS <<= 1
                            CS <<= 1
                            bit = next(bit_yield)
                            CS += bit
                    buffer[(1024 * i + j) * 3 + rgb] = byte
    except StopIteration:
        pass
    return buffer

if __name__ == '__main__':
    with open("data", 'rb') as fp:
        data = fp.read()

    bit_yield = get_bit(data[0x36:])
    buffer = decode(bit_yield)
    with open('data3', 'wb') as fp:
        fp.write(data[:0x36])
        fp.write(buffer)
```
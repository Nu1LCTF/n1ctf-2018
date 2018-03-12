#! usr/bin/python
def bit_fill(array):
    while True:
        ch = 0
        for i in range(8):
            bit = yield None
            # assert bit == 0 or bit == 1
            if bit == -1:
                array.append(ch)
                array.append(i)
            ch += bit << i
        array.append(ch)


def decode_img(img_data):
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

    img_head = img_data[:0x36]
    img_data = img_data[0x36:]
    assert len(img_data) == 1024 * 1024 * 3
    for rgb in range(3):
        for i in range(1024):
            # print(i)
            for j in range(1024):
                byte = img_data[(1024 * i + j) * 3 + rgb]
                sum1 = 0
                for x in range(4):
                    for y in range(4):
                        if x == 0 and y == 0:
                            continue
                        if i - x < 0 or j - y < 0:
                            ch = 0xff
                        else:
                            ch = img_data[(1024 * (i - x) + (j - y)) * 3 + rgb]
                        sum1 += bit_num[ch]
                if sum1 < 60:
                    H = 0
                    Q = q_list[sum1]
                else:
                    H = 1
                    Q = q_list[120 - sum1]
                for n in range(8):
                    bit = byte & 1
                    byte >>= 1
                    yield bit, Q, H


def encode(bit_yield, out_buf):
    set_trap = False
    trap_n = 0
    CS = 0
    AS = 0xff
    try:
        while True:
            bit, Q, H = next(bit_yield)

            AL = AS >> Q
            AH = AS - AL

            if bit == H:
                AS = AH
            else:
                AS = AL
                CS += AH

            if CS & 0x100:
                CS = CS & 0xff
                out_buf.send(1)
                if trap_n > 0:
                    for count in range(trap_n - 1):
                        out_buf.send(0)
                    trap_n = 0
                else:
                    set_trap = False
            while AS & 0x80 == 0:
                if CS & 0x80:
                    out_bit = 1
                    CS = CS & 0x7f
                else:
                    out_bit = 0

                if set_trap:
                    if out_bit == 1:
                        trap_n += 1
                    else:
                        out_buf.send(0)
                        for count in range(trap_n):
                            out_buf.send(1)
                        trap_n = 0
                else:
                    if out_bit == 1:
                        out_buf.send(1)
                    else:
                        set_trap = True
                AS <<= 1
                CS <<= 1

    except StopIteration:
        CS += 0x40
        if CS & 0x100:
            out_buf.send(1)
            for i in range(trap_n + 2):
                out_buf.send(0)
        elif set_trap:
            out_buf.send(0)
            for i in range(trap_n):
                out_buf.send(1)
            out_buf.send(1 if CS & 0x80 else 0)
            out_buf.send(1 if CS & 0x40 else 0)


if __name__ == '__main__':
    with open("timg.bmp", 'rb') as fp:
        data = fp.read()

    bit_yield = decode_img(data)
    buffer = bytearray()
    out_buf = bit_fill(buffer)
    out_buf.send(None)

    encode(bit_yield, out_buf)

    out_buf.send(-1)
    with open('data', 'wb') as fp:
        fp.write(data[:0x36])
        fp.write(buffer)

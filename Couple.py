__author__ = 'TheJoker'
from filetools import get_path
import xlrd
from math import (sqrt, pi, pow, log10)
from numpy import (exp, interp)


# fresnel_me test pass
def fresnel_me(x):
    n_x = int(pow(10, 6))
    delta = x / n_x
    x_t = [0]
    y = [complex(0, 0)]
    y_1 = [exp(y[0])]
    for i in range(0, n_x):
        x_t.append(delta * (i + 1))
        y.append(complex(0, 0.5 * pi * pow(delta * (i + 1), 2)))
        y_1.append(exp(y[i]))
    result = sum(y_1) * delta
    return result


def cal_field(freq, fieldintensity):
    """get the power meter power target, the """
    global antennaindex
    couplercal = get_path() + '/Data/CoupleCal.xlsx'
    # Coupler A: 800Mto4200M  Coupler B: 2Gto18G
    coupledata = xlrd.open_workbook(couplercal)
    couple_a_sheet = coupledata.sheet_by_index(3)
    couple_b_sheet = coupledata.sheet_by_index(2)
    couple_a = [couple_a_sheet.col_values(0)[8:3209]]
    couple_b = [couple_b_sheet.col_values(0)[8:1609]]
    # get the couple data range(3200, 3) (1600, 3)
    for i in range(1, 6):
        couple_a.append(couple_a_sheet.col_values(i)[8:3209])
        couple_b.append(couple_b_sheet.col_values(i)[8:1609])
    # get the horn data
    hornpath = get_path() + '/Data/ETS_horn.xlsx'
    hornxl = xlrd.open_workbook(hornpath)
    hornsheet = hornxl.sheet_by_index(0)
    antennadata = [hornsheet.col_values(0)[1:11]]
    for i in range(1, 12):
        antennadata.append(hornsheet.col_values(i)[1:11])
    # antenna index
    antennaname = int(antennadata[0][0])
    p_in = 1  # 端口的射频功率
    # confirm the antenna with suitable frequency
    if freq < 0.96 or freq > 18:
        return 'Wrong frequency input'
    elif freq == 0.96:
        antennaindex = 0
        pass
    else:
        for i in range(0, 10):
            if antennadata[1][i] < freq <= antennadata[2][i]:
                antennaname = int(antennadata[0][i])
                antennaindex = i
                break
            else:
                pass
    antenna = 'ETS3160-0' + str(antennaname)
    # calculate the s11
    vswr = antennadata[3][antennaindex]
    s11 = (vswr - 1) / (vswr + 1)
    factor_input = 1 - s11 * s11
    # 口径长边和短边
    a = antennadata[4][antennaindex] / 100
    b = antennadata[5][antennaindex] / 100
    le = antennadata[9][antennaindex] / 100
    lh = antennadata[10][antennaindex] / 100
    d = antennadata[11][antennaindex]  # 轴线上测量点到口面中心的距离
    le1 = d * le / (le + d)
    lh1 = d * lh / (lh + d)
    lam = 0.3 / freq
    w = b / sqrt(2 * lam * le1)
    u = sqrt(lam * lh1 * 0.5) / a + a / sqrt(2 * lam * lh1)
    v = sqrt(lam * lh1 * 0.5) / a - a / sqrt(2 * lam * lh1)

    c_w = fresnel_me(w).real
    s_w = fresnel_me(w).imag
    c_u = fresnel_me(u).real
    s_u = fresnel_me(u).imag
    c_v = fresnel_me(v).real
    s_v = fresnel_me(v).imag

    r_e = (pow(c_w, 2) + pow(s_w, 2)) / pow(w, 2)
    r_h = 0.25 * pow(pi, 2) * (pow(c_u - c_v, 2) + pow(s_u - s_v, 2)) / pow(u - v, 2)
    gain_0 = 32 * a * b / (pi * pow(lam, 2))  # 这个实际上也不是其远场增益
    gain_near = gain_0 * r_e * r_h  # 在设定条件下的近场增益
    e_cal_1w = sqrt(30 * gain_near * factor_input * p_in) / d

    # 以下进行功率计监控部分的处理   'A'代表0.8G-4.2G的耦合器，而'B'代表2G~18G的耦合器（带20dB衰减器）
    if freq > 4.2:
        coupler = 'B'

    elif freq <= 2:
        coupler = 'A'

    else:
        coupler = 'Wrong coupler'

    coupler_using = couple_a
    if coupler == 'A':  # 选择耦合器的数据
        coupler_using = couple_a
    elif coupler == 'B':  # 选择耦合器的数据
        coupler_using = couple_b

    # 以下进行功率计监控部分的处理
    freq_coupler = coupler_using[0]
    powerratio_db_coupler = coupler_using[5]  # 功率比值，dB
    freq *= pow(10, 9)
    power_ratio_antenna2pm_db = interp(freq, freq_coupler, powerratio_db_coupler)  # yi = interp1(x,Y,xi)
    pin_ambition = pow(fieldintensity * d, 2) / (30 * gain_near * factor_input)
    pin_ambition_dbm = 10 * log10(pin_ambition) + 30
    p_meter_disp_dbm = pin_ambition_dbm - power_ratio_antenna2pm_db  # 功率计上显示的功率值

    result = [p_meter_disp_dbm, coupler, antenna, e_cal_1w]
    return result


if __name__ == '__main__':
    print(cal_field(18, 30))

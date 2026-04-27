"""
anti_gravity_balance.py

用于计算科幻设定中的“重力—反重力平衡高度”。

模型：
    重力加速度：
        a_g(h) = g * (R / (R + h))^2

    反重力加速度：
        a_A(h) = sigma * exp(-h / H)

平衡条件：
        sigma * exp(-h / H) = g * (R / (R + h))^2

其中：
    h      : 地面以上高度，单位 m
    R      : 星球半径，单位 m
    g      : 地表重力加速度，单位 m/s^2
    sigma  : 地表反重力加速度，单位 m/s^2
    H      : 反重力衰减尺度，单位 m

运行：
    python anti_gravity_balance.py
"""

import math


# =========================
# 你可以手动修改这里的参数
# =========================

R = 6_371_000       # 星球半径，地球约 6,371,000 m
g = 9.80665         # 地表重力加速度，地球约 9.80665 m/s^2

sigma = 12.0        # 地表反重力加速度，必须大于 g 才能从地面起飞
H = 10_000          # 反重力衰减尺度，单位 m。越小，反重力衰减越快


# =========================
# 计算函数
# =========================

def gravity(h: float) -> float:
    """高度 h 处的重力加速度，方向向下。"""
    return g * (R / (R + h)) ** 2


def anti_gravity(h: float) -> float:
    """高度 h 处的反重力加速度，方向向上。"""
    return sigma * math.exp(-h / H)


def net_acceleration(h: float) -> float:
    """
    净加速度：向上为正。
    > 0：反重力更强，继续上升
    = 0：平衡
    < 0：重力更强，会下落
    """
    return anti_gravity(h) - gravity(h)


def find_balance_height(max_height: float = 1_000_000_000, tolerance: float = 1e-6) -> float | None:
    """
    用二分法寻找地面以上的平衡高度。

    max_height:
        搜索上限，默认 1e9 m，即一百万公里。
    tolerance:
        高度精度，单位 m。

    返回：
        平衡高度 h，单位 m。
        若不存在地面以上平衡点，返回 None。
    """

    # 地面反重力必须强于重力，否则无法从地面自然升起
    if net_acceleration(0) <= 0:
        return None

    low = 0.0
    high = H

    # 自动扩大搜索范围，直到净加速度变为负
    while net_acceleration(high) > 0:
        high *= 2

        if high > max_height:
            return None

    # 二分法求根
    while high - low > tolerance:
        mid = (low + high) / 2

        if net_acceleration(mid) > 0:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def approximate_balance_height() -> float | None:
    """
    近似公式：
        h ≈ H * ln(sigma / g)

    适用于 h << R 的情况。
    """
    if sigma <= g:
        return None

    return H * math.log(sigma / g)


# =========================
# 主程序
# =========================

if __name__ == "__main__":
    h_exact = find_balance_height()
    h_approx = approximate_balance_height()

    print("=== 重力—反重力平衡高度计算 ===")
    print(f"星球半径 R = {R:,.3f} m")
    print(f"地表重力 g = {g:.6f} m/s^2")
    print(f"地表反重力 sigma = {sigma:.6f} m/s^2")
    print(f"反重力衰减尺度 H = {H:,.3f} m")
    print()

    if h_exact is None:
        print("没有找到地面以上的平衡点。")
        print("可能原因：")
        print("1. sigma <= g，地面反重力不足以起飞；")
        print("2. 搜索范围内反重力始终强于重力；")
        print("3. 参数组合不产生有限平衡高度。")
    else:
        print(f"完整数值解：h = {h_exact:,.3f} m")
        print(f"完整数值解：h = {h_exact / 1_000:,.3f} km")
        print()

        if h_approx is not None:
            print(f"近似解：h ≈ {h_approx:,.3f} m")
            print(f"近似解：h ≈ {h_approx / 1_000:,.3f} km")
            print(f"近似误差：{abs(h_exact - h_approx):,.3f} m")

        print()
        print("平衡点处：")
        print(f"重力加速度     = {gravity(h_exact):.9f} m/s^2")
        print(f"反重力加速度   = {anti_gravity(h_exact):.9f} m/s^2")
        print(f"净加速度       = {net_acceleration(h_exact):.12f} m/s^2")

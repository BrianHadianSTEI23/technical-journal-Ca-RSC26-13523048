
import asyncio
from mavsdk import System
from mavsdk.offboard import PositionNedYaw, OffboardError


FIGURE_8_POINTS = [
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (2.5,   2.89, 0),
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (2.89,   2.5, 0),
    (5,   0, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
    (2.5,   -2.89, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
    (2.89,   -2.5, 0),
]


async def run():
    drone = System()
    await drone.connect(system_address="udp://:14550")

    async for state in drone.core.connection_state():
        if state.is_connected:
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            break

    print("arm...")
    await drone.action.arm()

    print("taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(8)

    await drone.offboard.set_position_ned(
        PositionNedYaw(0.0, 0.0, -15.0, 0.0)
    )

    try:
        await drone.offboard.start()
    except OffboardError as e:
        print(f"fail : {e._result.result}")
        return

    for i, (n, e, d) in enumerate(FIGURE_8_POINTS):
        print(f"wp {i+1}: {n} {e} {d}")
        await drone.offboard.set_position_ned(
            PositionNedYaw(n, e, d, 0.0)
        )
        await asyncio.sleep(4)

    await drone.offboard.stop()
    await drone.action.land()


if __name__ == "__main__":
    asyncio.run(run())

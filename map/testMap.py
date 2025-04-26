import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Polygon, Point
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

# Параметры карты (завод Азот, Кемерово)
center_lat, center_lon = 55.34917, 85.98411
rows = 2  # 2 строки
cols = 5  # 5 столбцов
sector_size = 0.0008  # Увеличенный размер сектора (~80 метров)

# Рассчитываем границы территории (больший охват)
min_lon = center_lon - (cols * sector_size)
max_lon = center_lon + (cols * sector_size)
min_lat = center_lat - (rows * sector_size)
max_lat = center_lat + (rows * sector_size)

# Создаем секторы по схеме:
sectors = {
    # Верхний ряд
    6: (center_lon - 2 * sector_size, center_lat + 0.5 * sector_size),
    5: (center_lon - 1 * sector_size, center_lat + 0.5 * sector_size),
    7: (center_lon + 0 * sector_size, center_lat + 0.5 * sector_size),
    8: (center_lon + 1 * sector_size, center_lat + 0.5 * sector_size),
    9: (center_lon + 2 * sector_size, center_lat + 0.5 * sector_size),

    # Нижний ряд
    1: (center_lon - 2 * sector_size, center_lat - 0.5 * sector_size),
    2: (center_lon - 1 * sector_size, center_lat - 0.5 * sector_size),
    3: (center_lon + 0 * sector_size, center_lat - 0.5 * sector_size),
    4: (center_lon + 1 * sector_size, center_lat - 0.5 * sector_size),
    10: (center_lon + 2 * sector_size, center_lat - 0.5 * sector_size)
}

# Создаем GeoDataFrame для секторов
gdf_sectors = gpd.GeoDataFrame(
    [
        {
            "id": sector_id,
            "geometry": Polygon([
                [lon, lat],
                [lon + sector_size, lat],
                [lon + sector_size, lat + sector_size],
                [lon, lat + sector_size],
            ]),
        }
        for sector_id, (lon, lat) in sectors.items()
    ],
    crs="EPSG:4326",
).to_crs(epsg=3857)

# Сотрудники (пример данных)
employees = [
    {"id": 10001, "sector_id": 1},
    {"id": 10002, "sector_id": 1},
    {"id": 10003, "sector_id": 5},
    {"id": 10004, "sector_id": 5},
    {"id": 10005, "sector_id": 7},
    {"id": 10006, "sector_id": 7},
    {"id": 10007, "sector_id": 10},
    {"id": 10008, "sector_id": 10},
    {"id": 10009, "sector_id": 10}
]


# Функция для распределения точек внутри сектора
def distribute_points_in_sector(sector_id, count):
    lon, lat = sectors[sector_id]
    center_x = lon + sector_size / 2
    center_y = lat + sector_size / 2
    radius = sector_size * 0.25  # Уменьшенный радиус распределения

    angles = np.linspace(0, 2 * np.pi, count, endpoint=False)
    offsets = np.column_stack([np.cos(angles), np.sin(angles)]) * radius

    return [(center_x + dx, center_y + dy) for dx, dy in offsets]


# Создаем точки для сотрудников
employee_points = []
for sector_id in set(emp["sector_id"] for emp in employees):
    sector_emps = [emp for emp in employees if emp["sector_id"] == sector_id]
    points = distribute_points_in_sector(sector_id, len(sector_emps))

    for emp, (lon, lat) in zip(sector_emps, points):
        employee_points.append({
            "id": emp["id"],
            "geometry": Point(lon, lat)
        })

# GeoDataFrame для сотрудников
gdf_employees = gpd.GeoDataFrame(
    employee_points,
    crs="EPSG:4326"
).to_crs(epsg=3857)

# Визуализация
fig, ax = plt.subplots(figsize=(18, 12))  # Увеличенный размер изображения

# Отрисовка секторов
gdf_sectors.boundary.plot(ax=ax, color="blue", linewidth=2, alpha=0.7)

# Номера секторов
for idx, row in gdf_sectors.iterrows():
    minx, miny, _, _ = row.geometry.bounds
    ax.annotate(
        text=str(row["id"]),
        xy=(minx + 20, miny + 20),
        ha="left", va="bottom",
        fontsize=11,
        color="black",
        weight="bold",
        backgroundcolor="white",
        alpha=0.9
    )

# Отрисовка сотрудников (уменьшенные кружки)
patches = [Circle((row.geometry.x, row.geometry.y), 20,
                  facecolor='red', edgecolor='white', alpha=0.8, linewidth=0.5)
           for _, row in gdf_employees.iterrows()]

ax.add_collection(PatchCollection(patches, match_original=True))

# Подписи сотрудников
for _, row in gdf_employees.iterrows():
    ax.annotate(
        text=str(row["id"]),
        xy=(row.geometry.x, row.geometry.y),
        ha="center", va="center",
        fontsize=8,
        color="white",
        weight="bold"
    )

# Добавляем подложку (меньший зум)
ctx.add_basemap(
    ax,
    source=ctx.providers.OpenStreetMap.Mapnik,
    alpha=0.8,
    zoom=16  # Уменьшенный зум для большего охвата
)

# Настройки
ax.set_axis_off()
plt.title("Завод 'Азот' (Кемерово)\nРаспределение сотрудников по секторам", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig("azot_final_map.png", dpi=300, bbox_inches="tight")
plt.close()
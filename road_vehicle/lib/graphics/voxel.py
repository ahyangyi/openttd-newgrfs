from agrf.graphics.voxel import LazyVoxel as LazyVoxelBase, LazySwitch, LazyAlternatives


# RV-specific hack
def LazyVoxel(name, load_from=None, **kwargs):
    if load_from is None:
        load_from = "road_vehicle/templates/manifest.json"
    return LazyVoxelBase(
        name,
        prefix=f"road_vehicle/voxels/render/{name}",
        voxel_getter=lambda: f"road_vehicle/voxels/{name}.vox",
        load_from=load_from,
        **kwargs,
    )

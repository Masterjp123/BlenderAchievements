# blender_achievements.py
# ============================================
# A lightweight, fully data-driven Blender add-on for achievements.
# Only the JSON files need updating to add or change achievements.

bl_info = {
    "name": "Achievements Add-on",
    "author": "Your Name",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Achievements",
    "description": "Tracks actions and awards achievements defined in JSON",
    "category": "3D View"
}

import bpy, os, json

# -------------------------
# Module-Level Data
# -------------------------

# Generic counters for event-based triggers
event_counters = {}
# Loaded achievements list
all_achievements = []
# Unlocked set
unlocked = set()

# -------------------------
# JSON Loading
# -------------------------

def get_addon_directory():
    return os.path.dirname(os.path.realpath(__file__))


def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Achievements] Failed to load {filepath}: {e}")
        return []


def load_achievements():
    prefs = bpy.context.preferences.addons[__name__].preferences
    base = get_addon_directory()
    achs = []
    # default file
    default_file = os.path.join(base, 'achievements', 'default.json')
    achs.extend(load_json(default_file))
    # community
    if prefs.enable_community:
        comm_dir = os.path.join(base, 'achievements', 'community')
        if os.path.isdir(comm_dir):
            for f in os.listdir(comm_dir):
                if f.lower().endswith('.json'):
                    achs.extend(load_json(os.path.join(comm_dir, f)))
    return achs

# -------------------------
# Trigger Getters
# -------------------------

def get_vertex_count():
    return sum(len(obj.data.vertices) for obj in bpy.data.objects if obj.type == 'MESH')

def get_collection_count():
    return len(bpy.data.collections)

def get_material_count():
    return len(bpy.data.materials)

def get_node_count():
    return sum(len(mat.node_tree.nodes) for mat in bpy.data.materials if mat.use_nodes)

# Generic handler for any event counter
def get_event_counter(name):
    return event_counters.get(name, 0)

# Map trigger names to getter functions
trigger_getters = {
    'vertex_count': get_vertex_count,
    'collection_count': get_collection_count,
    'material_count': get_material_count,
    'node_count': get_node_count,
    # event-based triggers via event_counters
    'save_count': lambda: get_event_counter('save_count'),
    'render_count': lambda: get_event_counter('render_count'),
    'object_created': lambda: get_event_counter('object_created'),
    # add more as needed...
}

# -------------------------
# Event Hooks
# -------------------------

def increment_counter(event_name):
    event_counters[event_name] = event_counters.get(event_name, 0) + 1

# Save event
def on_save(dummy):
    increment_counter('save_count')
bpy.app.handlers.save_post.append(on_save)

# Render complete event
def on_render(dummy):
    increment_counter('render_count')
bpy.app.handlers.render_complete.append(on_render)

# Object creation via depsgraph updates (approximate)
def on_depsgraph(scene, depsgraph):
    for update in depsgraph.updates:
        if isinstance(update.id, bpy.types.Object) and update.is_new:
            increment_counter('object_created')
bpy.app.handlers.depsgraph_update_post.append(on_depsgraph)

# -------------------------
# Achievement Logic
# -------------------------

def unlock_achievement(aid):
    unlocked.add(aid)
    bpy.ops.screen.display_notification('INVOKE_DEFAULT', message=f"🎉 Achievement Unlocked: {aid}")

# Timer check (runs every few seconds)
def check_achievements():
    for ach in all_achievements:
        aid = ach.get('id')
        if aid in unlocked:
            continue
        trig = ach.get('trigger')
        thresh = ach.get('threshold', 1)
        getter = trigger_getters.get(trig)
        if getter:
            try:
                value = getter()
                if value >= thresh:
                    unlock_achievement(aid)
            except Exception as e:
                print(f"[Achievements] Error checking {aid}: {e}")
    return 5.0

# -------------------------
# UI Panel & Operator
# -------------------------

class AchievementsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    enable_community: bpy.props.BoolProperty(
        name="Enable Community Achievements",
        default=False
    )
    def draw(self, context):
        self.layout.prop(self, "enable_community")

class SyncAchievementsOperator(bpy.types.Operator):
    bl_idname = 'achievements.sync'
    bl_label = 'Sync Achievements'
    def execute(self, context):
        global all_achievements, unlocked
        all_achievements = load_achievements()
        unlocked.clear()
        self.report({'INFO'}, f"Loaded {len(all_achievements)} achievements.")
        return {'FINISHED'}

class AchievementsPanel(bpy.types.Panel):
    bl_label = "Achievements"
    bl_idname = "VIEW3D_PT_achievements"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Achievements'
    def draw(self, context):
        layout = self.layout
        layout.operator('achievements.sync')
        for ach in all_achievements:
            label = ach.get('name', ach.get('id'))
            status = '✔' if ach.get('id') in unlocked else '  '
            layout.label(text=f"{status} {label}")

# -------------------------
# Register
# -------------------------
classes = [
    AchievementsPreferences,
    SyncAchievementsOperator,
    AchievementsPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # initial load and start timer
    global all_achievements
    all_achievements = load_achievements()
    bpy.app.timers.register(check_achievements, first_interval=5.0)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # handlers cleanup
    bpy.app.handlers.save_post.remove(on_save)
    bpy.app.handlers.render_complete.remove(on_render)
    bpy.app.handlers.depsgraph_update_post.remove(on_depsgraph)
    bpy.app.timers.unregister(check_achievements)

if __name__ == '__main__':
    register()

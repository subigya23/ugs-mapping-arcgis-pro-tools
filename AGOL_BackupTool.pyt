import arcpy
from arcgis.gis import GIS
import os
import time


class Toolbox(object):
    def __init__(self):
        self.label = "AGOL Folder Backup Toolbox"
        self.alias = "AGOLBackup"
        self.tools = [BackupAGOLData, BackupAGOLGroupData]


class BackupAGOLData(object):
    def __init__(self):
        self.label = "AGOL Folder Backup Tool"
        self.description = "Back up ArcGIS Online content and preserve folder structure locally."

    def getParameterInfo(self):
        output_folder = arcpy.Parameter(
            displayName="Output Folder (Local)",
            name="output_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        agol_folder = arcpy.Parameter(
            displayName="AGOL Folder Name(s) (Optional, comma-separated, leave empty for ALL folders)",
            name="agol_folder",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )

        export_feature_layers = arcpy.Parameter(
            displayName="Export Feature Layers",
            name="export_feature_layers",
            datatype="Boolean",
            parameterType="Optional",
            direction="Input"
        )
        export_feature_layers.value = False

        export_format = arcpy.Parameter(
            displayName="Feature Layer Export Format",
            name="export_format",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        export_format.filter.type = "ValueList"
        export_format.filter.list = [
            "File Geodatabase", "Shapefile", "CSV", "KML",
            "Excel", "GeoJson", "Feature Collection", "GeoPackage"
        ]
        export_format.enabled = False

        return [output_folder, agol_folder, export_feature_layers, export_format]

    def updateParameters(self, parameters):
        parameters[3].enabled = bool(parameters[2].value)
        return

    def execute(self, parameters, messages):
        output_folder = parameters[0].valueAsText
        selected_folder = parameters[1].valueAsText
        export_feature_layers = parameters[2].value
        export_format = parameters[3].valueAsText

        try:
            messages.addMessage("🔐 Connecting using ArcGIS Pro session...")
            gis = GIS("pro")
            user = gis.users.me
            if not user:
                messages.addErrorMessage("❌ No user signed in to ArcGIS Pro.")
                return

            messages.addMessage(f"👤 Signed in as: {user.username}")

            if selected_folder:
                all_folders = [f.strip() for f in selected_folder.split(",") if f.strip()]
            else:
                user_root = user.username
                all_folders = [user_root] + ([f['title'] for f in user.folders] if user.folders else [])

            for folder_name in all_folders:
                messages.addMessage(f"\n📁 Processing folder: '{folder_name}'")

                folder_param = None if folder_name == user.username else folder_name
                items = user.items(folder=folder_param, max_items=-1)

                if not items:
                    messages.addWarningMessage(f"⚠️ No items found in folder '{folder_name}'.")
                    continue

                local_folder = os.path.join(output_folder, folder_name)
                if not os.path.exists(local_folder):
                    os.makedirs(local_folder)

                messages.addMessage(f"📄 Found {len(items)} items.")

                for idx, item in enumerate(items, start=1):
                    item_type = item.type.lower()
                    title = item.title
                    messages.addMessage(f"\n📦 [{idx}/{len(items)}] Processing: {title} ({item.type})")

                    try:
                        if item_type in ["feature layer", "feature service"]:
                            if export_feature_layers and export_format:
                                safe_title = "".join(c if c.isalnum() else "_" for c in title)
                                timestamp = time.strftime("%Y%m%d")
                                export_title = f"{safe_title}_{timestamp}"
                                messages.addMessage(f"📤 Exporting Feature Layer as {export_format}...")
                                export_item = item.export(title=export_title, export_format=export_format)
                                messages.addMessage("⬇️ Downloading exported file...")
                                export_item.download(save_path=local_folder)
                                export_item.delete()
                                messages.addMessage("✅ Feature Layer exported and downloaded.")
                            else:
                                messages.addMessage("⬇️ Downloading Feature Layer item...")
                                item.download(save_path=local_folder)
                                messages.addMessage("✅ Feature Layer item downloaded.")
                        else:
                            messages.addMessage("⬇️ Downloading item...")
                            item.download(save_path=local_folder)
                            messages.addMessage("✅ Item downloaded.")
                    except Exception as e:
                        messages.addWarningMessage(f"⚠️ Could not process '{title}': {str(e)}")

            messages.addMessage("\n🎉 All folders backed up successfully!")

        except Exception as e:
            messages.addErrorMessage(f"❌ Critical error: {str(e)}")


class BackupAGOLGroupData(object):
    def __init__(self):
        self.label = "AGOL Group Backup Tool"
        self.description = "Back up ArcGIS Online group content."

    def getParameterInfo(self):
        output_folder = arcpy.Parameter(
            displayName="Output Folder (Local)",
            name="output_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        agol_group = arcpy.Parameter(
            displayName="AGOL Group Name(s) (comma-separated)",
            name="agol_group",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        export_feature_layers = arcpy.Parameter(
            displayName="Export Feature Layers",
            name="export_feature_layers",
            datatype="Boolean",
            parameterType="Optional",
            direction="Input"
        )
        export_feature_layers.value = False

        export_format = arcpy.Parameter(
            displayName="Feature Layer Export Format",
            name="export_format",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        export_format.filter.type = "ValueList"
        export_format.filter.list = [
            "File Geodatabase", "Shapefile", "CSV", "KML",
            "Excel", "GeoJson", "Feature Collection", "GeoPackage"
        ]
        export_format.enabled = False

        return [output_folder, agol_group, export_feature_layers, export_format]

    def updateParameters(self, parameters):
        parameters[3].enabled = bool(parameters[2].value)
        return

    def execute(self, parameters, messages):
        output_folder = parameters[0].valueAsText
        selected_groups = parameters[1].valueAsText
        export_feature_layers = parameters[2].value
        export_format = parameters[3].valueAsText

        try:
            messages.addMessage("🔐 Connecting using ArcGIS Pro session...")
            gis = GIS("pro")
            user = gis.users.me

            if not user:
                messages.addErrorMessage("❌ No user signed in to ArcGIS Pro.")
                return

            messages.addMessage(f"👤 Signed in as: {user.username}")

            group_list = [g.strip() for g in selected_groups.split(",") if g.strip()]

            for group_name in group_list:
                messages.addMessage(f"\n📁 Processing group: '{group_name}'")

                groups = gis.groups.search(f'title:\"{group_name}\"', max_groups=5)

                if not groups:
                    messages.addWarningMessage(f"⚠️ Group '{group_name}' not found.")
                    continue

                group = groups[0]
                items = group.content()

                if not items:
                    messages.addWarningMessage(f"⚠️ No items found in group '{group_name}'.")
                    continue

                local_folder = os.path.join(output_folder, group.title)
                os.makedirs(local_folder, exist_ok=True)

                messages.addMessage(f"📄 Found {len(items)} items.")

                for idx, item in enumerate(items, start=1):
                    item_type = item.type.lower()
                    title = item.title

                    messages.addMessage(f"\n📦 [{idx}/{len(items)}] Processing: {title} ({item.type})")

                    try:
                        if item_type in ["feature layer", "feature service"]:
                            if export_feature_layers and export_format:
                                safe_title = "".join(c if c.isalnum() else "_" for c in title)
                                timestamp = time.strftime("%Y%m%d")
                                export_title = f"{safe_title}_{timestamp}"

                                messages.addMessage(f"📤 Exporting Feature Layer as {export_format}...")
                                export_item = item.export(title=export_title, export_format=export_format)

                                messages.addMessage("⬇️ Downloading exported file...")
                                export_item.download(save_path=local_folder)

                                export_item.delete()

                                messages.addMessage("✅ Feature Layer exported and downloaded.")
                            else:
                                messages.addMessage("⬇️ Downloading Feature Layer item...")
                                item.download(save_path=local_folder)
                                messages.addMessage("✅ Feature Layer item downloaded.")
                        else:
                            messages.addMessage("⬇️ Downloading item...")
                            item.download(save_path=local_folder)
                            messages.addMessage("✅ Item downloaded.")

                    except Exception as e:
                        messages.addWarningMessage(f"⚠️ Could not process '{title}': {str(e)}")

            messages.addMessage("\n🎉 All groups backed up successfully!")

        except Exception as e:
            messages.addErrorMessage(f"❌ Critical error: {str(e)}")
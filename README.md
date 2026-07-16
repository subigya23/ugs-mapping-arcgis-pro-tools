# UGS Mapping ArcGIS Pro Tools

ArcGIS Pro Python tools for downloading and backing up ArcGIS Online content to a local directory.

## AGOL Backup Toolbox

`AGOL_BackupTool.pyt` is an ArcGIS Pro Python toolbox that connects to ArcGIS Online through the account currently signed in to ArcGIS Pro.

The toolbox includes two tools:

- **AGOL Folder Backup Tool**
- **AGOL Group Backup Tool**

## Features

- Backs up ArcGIS Online content owned by the signed-in user.
- Backs up content shared with ArcGIS Online groups.
- Preserves ArcGIS Online folder and group names as local folders.
- Supports multiple folder or group names entered as comma-separated values.
- Can export hosted feature layers before downloading them.
- Supports several feature-layer export formats.
- Displays progress, warnings, and errors in the ArcGIS Pro Geoprocessing pane.
- Continues processing remaining items when an individual item fails.

## Requirements

- ArcGIS Pro
- ArcGIS Pro signed in to ArcGIS Online
- Access to the folders, groups, and items being backed up
- ArcGIS API for Python
- ArcPy
- Permission to export hosted feature layers when using the export option

The toolbox connects to the active ArcGIS Pro session using:

```python
GIS("pro")
```

Users do not enter an ArcGIS Online username or password directly into the tool.

## Installation

1. Download `AGOL_BackupTool.pyt`.
2. Save the file in a permanent folder on your computer.
3. Open ArcGIS Pro.
4. Open the **Catalog** pane.
5. Right-click **Toolboxes**.
6. Select **Add Toolbox**.
7. Browse to `AGOL_BackupTool.pyt`.
8. Select the toolbox and click **OK**.

The following tools will appear:

- AGOL Folder Backup Tool
- AGOL Group Backup Tool

## AGOL Folder Backup Tool

The AGOL Folder Backup Tool downloads content owned by the ArcGIS Online user currently signed in through ArcGIS Pro.

### Parameters

#### Output Folder (Local)

Select the local folder where the backup will be saved.

#### AGOL Folder Name(s)

Enter one or more ArcGIS Online folder names separated by commas.

Example:

```text
Geologic Maps, Current Projects, Archived Data
```

Leave this parameter empty to process the user's root content and all ArcGIS Online folders.

The signed-in username is used as the local folder name for items stored in the ArcGIS Online root folder.

#### Export Feature Layers

Enable this option to export hosted feature layers before downloading them.

If this option is not enabled, the tool attempts to download the feature-layer item directly.

#### Feature Layer Export Format

When feature-layer export is enabled, choose one of the following formats:

- File Geodatabase
- Shapefile
- CSV
- KML
- Excel
- GeoJson
- Feature Collection
- GeoPackage

### Example

```text
Output Folder:
C:\AGOL_Backups

AGOL Folder Name(s):
Geologic Maps, Current Projects

Export Feature Layers:
True

Feature Layer Export Format:
File Geodatabase
```

### Example Output Structure

```text
C:\AGOL_Backups
├── username
│   └── root-folder items
├── Geologic Maps
│   └── downloaded items
└── Current Projects
    └── downloaded items
```

## AGOL Group Backup Tool

The AGOL Group Backup Tool downloads content shared with one or more ArcGIS Online groups.

### Parameters

#### Output Folder (Local)

Select the local folder where the group backups will be saved.

#### AGOL Group Name(s)

Enter one or more ArcGIS Online group names separated by commas.

Example:

```text
Geologic Mapping Team, Published Maps
```

The tool searches ArcGIS Online for each group title and uses the first matching search result.

#### Export Feature Layers

Enable this option to export hosted feature layers before downloading them.

#### Feature Layer Export Format

When feature-layer export is enabled, select the desired export format.

### Example

```text
Output Folder:
C:\AGOL_Group_Backups

AGOL Group Name(s):
Geologic Mapping Team, Published Maps

Export Feature Layers:
True

Feature Layer Export Format:
File Geodatabase
```

### Example Output Structure

```text
C:\AGOL_Group_Backups
├── Geologic Mapping Team
│   └── downloaded items
└── Published Maps
    └── downloaded items
```

## Feature-Layer Export Process

When feature-layer export is enabled, the toolbox performs the following steps:

1. Creates a temporary exported item in ArcGIS Online.
2. Downloads the exported file to the selected local folder.
3. Deletes the temporary exported item from ArcGIS Online.

The exported item name includes the current date.

Example:

```text
Geologic_Map_Index_20260716
```

Spaces and special characters in item titles are replaced with underscores.

## Messages and Error Handling

The toolbox reports progress in the ArcGIS Pro Geoprocessing pane.

Messages include:

- Connection status
- Signed-in ArcGIS Online username
- Folder or group currently being processed
- Number of items found
- Item title and item type
- Download and export progress
- Successful downloads
- Items that could not be processed
- Critical connection or execution errors

If an individual item fails, the tool displays a warning and continues processing the remaining items.

## Limitations

- Only content accessible to the signed-in ArcGIS Online account can be processed.
- Some ArcGIS Online item types cannot be downloaded directly.
- Downloaded items may not include all related dependencies.
- Web maps and applications may reference layers, services, URLs, or configuration resources that are not fully preserved by a basic download.
- Group searches are based on the group title, and the first matching result is used.
- Groups with identical or similar names may require additional verification.
- Exporting hosted feature layers depends on the user's permissions and the item's export settings.
- Feature-layer exports create temporary items in ArcGIS Online before downloading them.
- Item ownership, sharing settings, group membership, and other ArcGIS Online properties are not recreated locally.
- The toolbox does not currently include an automated restore process.
- The toolbox does not create a backup manifest or checksum report.
- Existing files with similar names may require manual review.

This toolbox should not be treated as a complete disaster-recovery solution.

## Recommended Practices

- Test the toolbox on a small folder or group first.
- Use a new date-specific output folder for each backup.
- Review all warnings after the tool finishes.
- Verify that downloaded files can be opened successfully.
- Confirm that important web maps and applications still have their required dependencies.
- Store backups in an approved and secure location.
- Follow organizational data-retention and information-security policies.
- Do not store confidential content in an unauthorized location.

Example backup folder:

```text
C:\AGOL_Backups\2026-07-16
```

## Download

To download the toolbox:

1. Click the green **Code** button.
2. Select **Download ZIP**.
3. Extract the downloaded ZIP file.
4. Add `AGOL_BackupTool.pyt` to ArcGIS Pro.

## Status

This project is under development.

The toolbox should be thoroughly tested before production use or official organizational distribution.

## License

No software license has been selected yet.

An organization-approved license should be added before public distribution.

## Disclaimer

This tool is provided without a guarantee that every ArcGIS Online item can be downloaded, exported, restored, or reproduced.

Users are responsible for validating their backups and following applicable organizational policies.

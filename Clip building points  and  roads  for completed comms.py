import arcpy
from arcgisscripting import da
import os
import re

pattern = re.compile('\W+')

# Set up the environment settings
arcpy.env.workspace = r"C:\Users\Shakeel.Hosein\Documents\ArcGIS\Projects\Community_Mapping\Community_Mapping.gdb "
arcpy.env.overwriteOutput = True

# The polygon feature class within the local geo-database(Community_Mapping.gdb) containing all of the
# communities that divide the entire of Tobago.
master_layer = 'Tobago_Communities'

# The point feature class within the local geo-database(Community_Mapping.gdb) containing the all of the
# property/building points for the entire country of Trinidad and Tobago
points_layer = 'Baseline_Surveys_Local'

# The line feature class within the local geo-database(Community_Mapping.gdb) containing all of the
# roads in the entire country of Trinidad and and Tobago
roads_layer = 'Roads_Local'

# A List of community names from the 'comm_name' field in the 'Tobago_Communities' feature class (above) referring
# to the communities to be used in the analysis
completed_comms = ["Fairways", "St. Clair", "Federation Park", "Ellerslie Park", "West Moorings", "Goodwood Gardens",
                   "Diego Martin Proper", "Bayshore", "Glencoe", "Victoria Gardens", "Alyce Glen", "Four Roads",
                   "Blue Range", "Barataria", "Tacarigua", "Dinsley", "Cane Farm", "Dinsley/Trincity", "Trincity",
                   "El Dorado", "Arima Proper", "Malabar", "O'meara Road", "Tumpuna Road", "Olton Road", "Guaico",
                   "Maraj Hill", "Sangre Grande", "St. Andrew's Village", "Couva Central", "Point Lisas (PLIPDECO)",
                   "Point Lisas (NHA)", "Cocoyea Village", "Debe Proper", "Gulf View", "Pleasantville",
                   "Les Efforts East", "Les Efforts West", "Penal",
                   "Penal Rock Road", "Macoya", "Bon Accord", "Buccoo/Coral Gardens", "Crown Point",
                   "Milford Court/Pigeon Pt.", "Canaan", "Scarborough"]


# Function to separate out the individual communities from the communities dataset that are only in the
# completed coms list then use that community polygon to clip the building point dataset and roads dataset

def separte_coms(all_coms):
    arcpy.management.MakeFeatureLayer(all_coms, 'all_coms_layer')
    fields = ['OBJECTID', 'COMM_Code', 'comm_name']
    cursor = arcpy.da.SearchCursor('all_coms_layer', fields)
    for row in cursor:
        if row[2] in completed_comms:
            boundary = arcpy.SelectLayerByAttribute_management('all_coms_layer', 'NEW_SELECTION', 'OBJECTID = {}'.format(row[0]))
            arcpy.analysis.Clip(points_layer, boundary, re.sub(pattern, '_', '{}_Building_Baseline_'.format(row[2])), None)
            arcpy.analysis.Clip(roads_layer, boundary, re.sub(pattern, '_', '{}_Roads_'.format(row[2])), None)
            print("{}_roads_complete".format(row[2]))


separte_coms(master_layer)

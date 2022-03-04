AGG_MEAN = "Mean"
AGG_STD_DEV = "StDev"
AGG_MEDIAN = "Median"
AGG_NAMES = [AGG_MEAN, AGG_MEDIAN, AGG_STD_DEV]
IMAGE = "Image"
EXPERIMENT = "Experiment"
RELATIONSHIP = "Relationship"
NEIGHBORS = "Neighbors"
OBJECT = "Object"
disallowed_object_names = [IMAGE, EXPERIMENT, RELATIONSHIP]
COLTYPE_INTEGER = "integer"
COLTYPE_FLOAT = "float"
COLTYPE_BLOB = "blob"
COLTYPE_MEDIUMBLOB = "mediumblob"
COLTYPE_LONGBLOB = "longblob"
COLTYPE_VARCHAR_FORMAT = "varchar(%d)"
COLTYPE_VARCHAR = "varchar"
PATH_NAME_LENGTH = 256
FILE_NAME_LENGTH = 128
COLTYPE_VARCHAR_FILE_NAME = COLTYPE_VARCHAR_FORMAT % FILE_NAME_LENGTH
COLTYPE_VARCHAR_PATH_NAME = COLTYPE_VARCHAR_FORMAT % PATH_NAME_LENGTH
MCA_AVAILABLE_EACH_CYCLE = "AvailableEachCycle"
MCA_AVAILABLE_POST_GROUP = "AvailablePostGroup"
MCA_AVAILABLE_POST_RUN = "AvailablePostRun"
C_METADATA = "Metadata"
FTR_SITE = "Site"
FTR_WELL = "Well"
FTR_ROW = "Row"
FTR_COLUMN = "Column"
FTR_PLATE = "Plate"
MEASUREMENTS_GROUP_NAME = "Measurements"
IMAGE_NUMBER = "ImageNumber"
OBJECT_NUMBER = "ObjectNumber"
GROUP_NUMBER = "Group_Number"  # 1-based group index
GROUP_INDEX = "Group_Index"  # 1-based index within group
R_FIRST_IMAGE_NUMBER = IMAGE_NUMBER + "_" + "First"
R_FIRST_OBJECT_NUMBER = OBJECT_NUMBER + "_" + "First"
R_SECOND_IMAGE_NUMBER = IMAGE_NUMBER + "_" + "Second"
R_SECOND_OBJECT_NUMBER = OBJECT_NUMBER + "_" + "Second"
C_FILE_NAME = "FileName"
C_PATH_NAME = "PathName"
C_URL = "URL"
C_SERIES = "Series"
C_FRAME = "Frame"
C_FRAMES = "Frames"
C_CHANNEL = "Channel"
C_Z = "ZPlane"
C_T = "Timepoint"
C_OBJECTS_FILE_NAME = "ObjectsFileName"
C_OBJECTS_PATH_NAME = "ObjectsPathName"
C_OBJECTS_URL = "ObjectsURL"
C_OBJECTS_SERIES = "ObjectsSeries"
C_OBJECTS_FRAME = "ObjectsFrame"
C_OBJECTS_CHANNEL = "ObjectsChannel"
C_OBJECTS_Z = "ObjectsZPlane"
C_OBJECTS_T = "ObjectsTimepoint"
C_CHANNEL_TYPE = "ChannelType"
C_FILE_LOCATION = "File_Location"
M_METADATA_TAGS = "_".join((C_METADATA, "Tags"))
M_GROUPING_TAGS = "_".join((C_METADATA, "GroupingTags"))
RESERVED_METADATA_TAGS = (
    "C",
    "T",
    "Z",
    "ColorFormat",
    "ChannelName",
    C_SERIES,
    C_FRAME,
    C_FILE_LOCATION,
)
M_PATH_MAPPINGS = "Path_Mappings"
K_CASE_SENSITIVE = "CaseSensitive"
K_PATH_MAPPINGS = "PathMappings"
K_LOCAL_SEPARATOR = "LocalSeparator"
K_URL2PATHNAME_PACKAGE_NAME = "Url2PathnamePackageName"
F_BATCH_DATA = "Batch_data.mat"
F_BATCH_DATA_H5 = "Batch_data.h5"
C_LOCATION = "Location"
C_NUMBER = "Number"
C_COUNT = "Count"
C_THRESHOLD = "Threshold"
C_PARENT = "Parent"
R_PARENT = "Parent"
C_CHILDREN = "Children"
R_CHILD = "Child"
FTR_CENTER_X = "Center_X"
M_LOCATION_CENTER_X = "%s_%s" % (C_LOCATION, FTR_CENTER_X)
FTR_CENTER_Y = "Center_Y"
M_LOCATION_CENTER_Y = "%s_%s" % (C_LOCATION, FTR_CENTER_Y)
FTR_CENTER_Z = "Center_Z"
M_LOCATION_CENTER_Z = "%s_%s" % (C_LOCATION, FTR_CENTER_Z)
FTR_OBJECT_NUMBER = "Object_Number"
M_NUMBER_OBJECT_NUMBER = "%s_%s" % (C_NUMBER, FTR_OBJECT_NUMBER)
FF_COUNT = "%s_%%s" % C_COUNT
FTR_FINAL_THRESHOLD = "FinalThreshold"
FF_FINAL_THRESHOLD = "%s_%s_%%s" % (C_THRESHOLD, FTR_FINAL_THRESHOLD)
FTR_ORIG_THRESHOLD = "OrigThreshold"
FF_ORIG_THRESHOLD = "%s_%s_%%s" % (C_THRESHOLD, FTR_ORIG_THRESHOLD)
FTR_GUIDE_THRESHOLD = "GuideThreshold"
FF_GUIDE_THRESHOLD = "%s_%s_%%s" % (C_THRESHOLD, FTR_GUIDE_THRESHOLD)
FTR_WEIGHTED_VARIANCE = "WeightedVariance"
FF_WEIGHTED_VARIANCE = "%s_%s_%%s" % (C_THRESHOLD, FTR_WEIGHTED_VARIANCE)
FTR_SUM_OF_ENTROPIES = "SumOfEntropies"
FF_SUM_OF_ENTROPIES = "%s_%s_%%s" % (C_THRESHOLD, FTR_SUM_OF_ENTROPIES)
FF_CHILDREN_COUNT = "%s_%%s_Count" % C_CHILDREN
FF_PARENT = "%s_%%s" % C_PARENT
M_SITE, M_WELL, M_ROW, M_COLUMN, M_PLATE = [
    "_".join((C_METADATA, x))
    for x in (FTR_SITE, FTR_WELL, FTR_ROW, FTR_COLUMN, FTR_PLATE)
]

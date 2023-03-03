
#allbigETFs = open("allbigETFs.txt")
#data_all = allbigETFs.read()
#list_all = data_all.split()
negative_files = ["meta", "xom"]
positive_files = ["tsla", "coin"]
multidata_file = "expense ratios"


def format_to_openable(x):
    y = x + ".txt"
    return y

#reads a file to a list of lines, which are themselves split into lists of elements
def read_txt_to_list(file):
    split_list=[]
    open_file = open(file)
    lines_in_file = open_file.readlines()
    for line in lines_in_file:
        elements_in_lines = line.split("\t")
        split_list.append(elements_in_lines)
    return split_list



#creates one list of all excluded etf by by merging all the exclusion files
def listing_excluded_etfs(negative_files):
    list_negative_etfs = []
    for file in negative_files:
        openable_negative_file = format_to_openable(file)
        negative_etfs_w_data = read_txt_to_list(openable_negative_file)
        for line in negative_etfs_w_data:
            etf = line[0]
            list_negative_etfs.append(etf)
    return list_negative_etfs


#removes element that are in the list of excluded etfs from the list of included etfs
def inclusion_list(inclusion_files):
    list_included_etfs = []
    filtered_positive_list = []
    for file in inclusion_files:
        openable_inclusion_file = format_to_openable(file)
        included_etfs_w_data = read_txt_to_list(openable_inclusion_file)
        for line in included_etfs_w_data:
            etf = line[0].strip()
            list_included_etfs.append(etf)
    x = len(inclusion_files)
    for etf in list_included_etfs:
        if list_included_etfs.count(etf) == x:
            filtered_positive_list.append(etf)
    return filtered_positive_list


def negative_filter(multidata_file, exclusion_files):
    excluded_etfs = listing_excluded_etfs(exclusion_files)
    neg_filtered_etfs = read_txt_to_list(format_to_openable(multidata_file))
    for list in neg_filtered_etfs:
        if list[0] in excluded_etfs:
            neg_filtered_etfs.remove(list)
    return neg_filtered_etfs


def neg_and_pos_filter(multidata_file, exclusion_files, inclusion_files):
    cross_list = []
    neg_filtered_etfs = negative_filter(multidata_file, exclusion_files)
    pos_filtered_etfs = inclusion_list(inclusion_files)
    for list in neg_filtered_etfs:
        if list[0] in pos_filtered_etfs:
            cross_list.append(list)
    return cross_list


def requested_elements_list():
    requested_list = neg_and_pos_filter(multidata_file, negative_files, positive_files)
    requested_elements = []
    for list in requested_list:
        element = list[0], list[4]
        requested_elements.append(element)
    return requested_elements

#print(*requested_elements_list(), sep = "\n")

def points(files):
    etfs_in_files = []
    etf_points = []
    for file in files:
        openable_negative_file = format_to_openable(file)
        negative_etfs_w_data = read_txt_to_list(openable_negative_file)
        etfs_in_files.append(negative_etfs_w_data)
    for file in etfs_in_files:
        individual_file_w_points = []
        for line in file:
            points = line[2].strip()
            points_clean = points.replace('%', '')
            points_number = float(points_clean)
            etf = line[0].strip()
            individual_file_w_points.append((etf, points_number))
        etf_points.append(individual_file_w_points)
    return etf_points

#print(points(positive_files))

def score():
    all_etfs = read_txt_to_list(format_to_openable(multidata_file))
    neg_etfs_w_points = (points(negative_files))
    pos_etfs_w_points = (points(positive_files))

    for list in all_etfs:
        etf = list[0]
        x = 0
        for file_list in neg_etfs_w_points:
            file_dict = dict(file_list)
            for key,value in file_dict.items():
                if key == etf:
                    x = x - value
        for file_list in pos_etfs_w_points:
            file_dict = dict(file_list)
            for key,value in file_dict.items():
                if key == etf:
                    x = x + value
        list.append(x)
    return all_etfs
#print(score())

def selection():
    all_etfs_w_score = score()
    positive_score_etfs = []
    clean_positive_score = []
    for list in all_etfs_w_score:
        x = list[6]
        if x > 0:
            positive_score_etfs.append(list)
    for list in positive_score_etfs:
        element = list[0], list[4], list[6]
        clean_positive_score.append(element)
    return clean_positive_score

print(*selection(), sep = "\n")
        
#print(score())




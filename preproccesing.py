import pandas as pd
import re

def process(data):
    """
    1. 기사 목록들로부터 중복 기사들을 유니크하게 만들고,
    2. 각 기사 제목으로부터 '[포토 뉴스]'와 같은 헤더를 지우고,
    3. 모든 특수문자를 지움.
    * 순서 바뀌면 안됨
    :param data: pandas dataframe
    :return : 전처리 완료된 기사 정보(제목, 추출된 명사들, 게시 시간) 목록
    """
    unique_data = to_unique(data)
    processed_data = pd.DataFrame(columns=['title', 'noun_title', 'created_at'])
    for idx, row in unique_data.iterrows():
        minutes_ago = get_time_offset(row['time_offset'])
        if minutes_ago > 3:  # 3분 전보다 이전에 작성한 기사들은 무시(중복 제거를 위함)
            continue
        header_removed = remove_header(row['title'])
        processed_title = remove_specialChar(header_removed)
        processed_noun_title = get_noun_of_title(processed_title)
        processed_data.loc[len(processed_data)] = [processed_title, processed_noun_title, row['created_at']]
    return processed_data

def process_and_merge(data, now):
    """
    1. 기사 목록들로부터 중복 기사들을 유니크하게 만들고,
    2. 각 기사 제목으로부터 '[포토 뉴스]'와 같은 헤더를 지우고,
    3. 모든 특수문자를 지움.
    * 순서 바뀌면 안됨
    :param data: pandas dataframe
    :return : 전처리 완료된 기사 정보(기사 제목들, 모든 기사들로부터 추출된 명사들, 수집 시간(now)) 행 1개
    """
    unique_data = to_unique(data)
    processed_data = pd.DataFrame(columns=['title', 'noun_title', 'created_at'])
    processed_titles = ''
    processed_noun_titles = ''
    for idx, row in unique_data.iterrows():
        minutes_ago = get_time_offset(row['time_offset'])
        if minutes_ago > 3:  # 3분 전보다 이전에 작성한 기사들은 무시(중복 제거를 위함)
            continue
        header_removed = remove_header(row['title'])
        processed_title = remove_specialChar(header_removed)
        processed_titles += processed_title
        processed_noun_titles += get_noun_of_title(processed_title)
    processed_data.loc[len(processed_data)] = [processed_titles, processed_noun_titles, now]
    return processed_data


def get_noun_of_title(title):
    from konlpy.tag import Okt
    Okt = Okt()
    nouns = Okt.nouns(title)
    return ' '.join(nouns)


def get_time_offset(data):
    """
    :param data: pandas dataframe
    :return: e.g.) 3분 전 -> 3 return
    """
    return int(data[:-3])


def to_unique(data):
    """
    data의 title속성이 중복인 행 제거
    :param data: pandas dataframe
    :return: unique data
    """
    return data.drop_duplicates(subset='title')


def remove_header(title):
    """
    기사 제목으로부터 '[포토 뉴스]', '[카드 뉴스]'와 같은 헤더를 지움
    :param title:
    :return 헤더를 지운 기사 제목:
    """
    pattern = r'\[[^]]*\]'
    return re.sub(pattern=pattern, repl='', string=title)


def remove_specialChar(title):
    """
    기사 제목으로부터 모든 특수 문자("-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·")를 지움
    :param title:
    :return 특수 문자를 지운 기사 제목:
    """
    pattern = '[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]'
    return re.sub(pattern=pattern, repl='', string=title)


def print_title_dataFrame(data):
    """
    데이터프레임 출력 함수
    :param data: pandas dataFrame
    :return: None
    """
    # data = pd.read_csv('results2.csv')
    # processed = process(data)
    for idx, row in data.iterrows():
        print(idx)
        print(row['title'])
        print(row['noun_title'])
        print(row['created_at'])
        print()
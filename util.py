import numpy as np


def split_text(s):
    return s.replace('[', '').replace(']', '').replace('\'', '').split(', ')


# Tra ve mot dictionary, key = id, value = [rating trung binhf, rating max, rating min]
# Dau vao la 2 column ids va rating
def getScoreBroad(broad_ids, movie_rating):
    cnt = {}
    tong = {}
    for i in range(len(movie_rating)):
        ids = str(broad_ids[i])
        ids = ids.replace('\'', '').replace('[', '').replace(']', '').split(sep=', ')

        for ids in ids:
            if ids == '':
                continue
            if cnt.get(ids) is None:  # khong co trong dict
                cnt[ids] = 1
                tong[ids] = [float(movie_rating[i])] * 3
            else:
                cnt[ids] += 1  # dem so luong
                tong[ids][0] += movie_rating[i]  # tong
                tong[ids][1] = max(tong[ids][1], movie_rating[i])  # max
                tong[ids][2] = min(tong[ids][2], movie_rating[2])  # min

    for ids in cnt:
        tong[ids][0] = tong[ids][0] / cnt[ids]  # lay trung binh

    return tong


# Tra ve mot tuple [score trung binh, socre max cua lead, score min cua lead]
# Lead la nguoi co score trung binh lon nhat
# Dau vao la danh sach ids va dictionary
def getScore(ids, scoreBroad):
    re = 0
    lead_score = -1
    lead_id = 0
    cnt = 0;
    ids = str(ids)
    ids = ids.replace('\'', '').replace('[', '').replace(']', '').split(sep=', ')
    for index in ids:
        if (scoreBroad.get(index) is not None) and (int(index) != 0):
            cnt += 1
            re += scoreBroad[index][0]
            if scoreBroad[index][0] > lead_score:
                lead_score = scoreBroad[index][0]
                lead_id = index

    if cnt == 0:
        return [np.nan] * 3

    mean_score, max_score, min_score = re / cnt, scoreBroad[lead_id][1], scoreBroad[lead_id][2]
    return mean_score, max_score, min_score


# Chuyen string thanh list
def apply_genre(s):
    s = str(s)
    s = s.replace('\'', '').replace('[', '').replace(']', '').split(sep=', ')
    return s


# Tra ve danh sach gom tat ca cac genre
# Dau vao la danh sach genre cua tat ca cac phim
def getGenres(mgenre):
    mlist = []
    for i in range(len(mgenre)):
        mlist.extend(mgenre[i])
    genres = list(set(mlist))
    return genres


# Tra ve ones_hot vector tuong ung voi danh sach genre
# Dau vao la danh sach genre can ones_hot va danh sach tat ca genre
def getBow(genreList, genres):
    genre_bow = np.zeros(len(genres) + 1)
    cnt = 0

    for i in range(len(genres)):
        if genres[i] in genreList:
            genre_bow[i] = 1
            cnt += 1

    if cnt < len(genreList):
        genre_bow[-1] = 1

    return genre_bow

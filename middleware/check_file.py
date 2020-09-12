# 拡張子の確認
def allwed_file(filename, cfg):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in cfg['ALLOWED_EXTENSIONS']

if __name__ == "__main__":
    pass
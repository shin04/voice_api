import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def change_dict_key(d, old_key, new_key, default_value=None):
    d[new_key] = d.pop(old_key, default_value)


# def preprocessing():
#     # dictのkeyをunicodeに


def upload_results(results, people_num):
    # Use a service account
    cred = credentials.Certificate('credentials/service-account.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    doc_ref = db.document(u'users/idid/records/record-id')
    doc_ref.set({
        u'stringExample': u'Hello, World!',
        u'booleanExample': True,
        u'numberExample': 3.14159265,
        u'arrayExample': [5, True, u'hello'],
        u'nullExample': None,
        u'objectExample': {
            u'a': 5,
            u'b': True
        }
    })

    # if people_num == 1:
    #     doc_ref = db.document(u'users/idid/records/record-id')
    #     doc_ref.set({
    #         u'speaking_times': results['speaking_time'][0][1],
    #         u'amplitude': results['amplitude'][0]['1'],
    #         u'pitch': results['pitch'][0]['1'],
    #         u'speaking_rate': results['speaking_rate'][0]['1']
    #     })
    # else:
    #     # 二人以上の時どうするー？
    #     print('error')


if __name__ == "__main__":
    pass

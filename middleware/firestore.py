import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def upload_speaking_time(arraies, size, doc_ref, field_name):
    for array in arraies:
        if type(array) != list:
            array = [array]
        doc_ref.update({field_name: firestore.ArrayUnion(array)})


def upload_array(arraies, size, doc_ref, field_name):
    ite = 0
    for i in range(0, len(arraies), size):
        field = field_name+str(ite)
        print(field)
        print(len(arraies[i:i+size]))
        doc_ref.update(
            {field: firestore.ArrayUnion(arraies[i:i+size])})
        ite += 1


def upload_results(results, people_num, user_id, record_id):
    # Use a service account
    cred = credentials.Certificate('credentials/service-account.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    endpoint = u'users/{}/records/{}/results/voice'.format(
        user_id, record_id)

    doc_ref = db.document(endpoint)
    doc_ref.set({
        u'speaking_times': [],
        u'amplitude': [],
        u'pitch': [],
        u'speaking_rate': results['speaking_rate']['1']
    })

    upload_speaking_time(results['speaking_time']
                         [1], 1, doc_ref, 'speaking_time')
    for i, amplitude in enumerate(results['amplitude']['1']):
        upload_array(amplitude, 15000, doc_ref, 'amplitude_{}'.format(i))

    # doc_ref.set({
    #     u'speaking_times': results['speaking_time'],
    #     u'amplitude': results['amplitude'],
    #     u'pitch': results['pitch'],
    #     u'speaking_rate': results['speaking_rate']
    # })

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

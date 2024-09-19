__author__ = 'elliotthall'

def get_auth_field(typename):
    if typename == "Ethnic label":
        authOrder = 'factoidlocation__location'
    elif typename == "Location":
        authOrder = 'factoidlocation__location'
    elif typename == "Dignity/Office":
        authOrder = 'dignityfactoid__dignityoffice'
    elif typename == "Occupation/Vocation":
        authOrder = 'occupationfactoid__occupation'
    elif typename == "Language Skill":
        authOrder = 'langfactoid__languageskill'
    elif typename == "Alternative Name":
        authOrder = 'vnamefactoid__variantname'
    elif typename == "Religion":
        authOrder = 'religionfactoid__religion'
    elif typename == "Possession":
        authOrder = 'possessionfactoid'
    elif typename == "Second Name":
        authOrder = 'famnamefactoid__familyname'
    elif typename == "Kinship":
        authOrder = 'kinfactoid__kinship'
    elif typename == "Narrative":
        authOrder = 'scdate'
    else:
        # todo may be scdate
        authOrder = "engdesc"
    return authOrder
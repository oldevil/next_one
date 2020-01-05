class Type:
    SUCCESS = 'success'
    ERROR = 'error'


class Success:
    PATIENT_CREATED = '患者创建成功'
    PATIENT_EDITED = '患者修改成功'
    PATIENT_GOT_IN = '患者接入成功'
    PATIENT_DELETED = '患者删除成功'
    PATIENT_GOT_DELETED = '已接患者全部删除成功'

    SURGEON_CREATED = '术者创建成功'
    SURGEON_EDITED = '术者修改成功'
    SURGEON_DELETED = '术者删除成功'

    ASSISTANT_CREATED = '一助创建成功'
    ASSISTANT_EDITED = '一助修改成功'
    ASSISTANT_DELETED = '一助删除成功'

    ROOM_QUEUE_UPDATED = '未接患者队列更新成功'
    ROOM_ROLL_BACKED = '已接患者回滚成功'


class Error:
    pass

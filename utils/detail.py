class Type:
    SUCCESS = 'success'
    ERROR = 'error'


class Success:
    PATIENT_CREATED = '患者创建成功'
    PATIENT_EDITED = '患者修改成功'
    PATIENT_GOT_IN = '患者接入成功'
    PATIENT_DELETED = '患者删除成功'
    PATIENT_GOT_DELETED = '已接患者全部删除成功'
    PATIENT_TOMORROW_QUEUE_CHECKED = '明日手术患者检查成功'
    PATIENT_PROJECT_CHECKED = '计划手术患者检查成功'
    PATIENT_DAILY_CHECKED = '患者每日检查成功'

    SURGEON_CREATED = '术者创建成功'
    SURGEON_EDITED = '术者修改成功'
    SURGEON_DELETED = '术者删除成功'

    ASSISTANT_CREATED = '一助创建成功'
    ASSISTANT_EDITED = '一助修改成功'
    ASSISTANT_DELETED = '一助删除成功'

    ROOM_QUEUE_UPDATED = '患者队列更新成功'


class Error:
    PATIENT_NOT_EXIST = '患者不存在'
    PATIENT_NOT_IN_QUEUE = '患者不在未接队列首位'
    PATIENT_ALREADY_DELETED = '患者已被删除'
    PATIENT_MOVED = '患者不在该术间'

    SURGEON_ALREADY_DELETED = '术者已被删除'

    ASSISTANT_ALREADY_DELETED = '一助已被删除'

    ROOM_BLOCKING = '术间正在排序'
    ROOM_SORTING_TIMEOUT = '术间排序超时'


class Message:
    PATIENT_NOT_EXIST = '患者不存在，可能已被删除'
    PATIENT_NOT_IN_QUEUE = '患者不在未接队列首位，可能已被移动'
    PATIENT_ALREADY_DELETED = '患者已被其他人删除'
    PATIENT_MOVED = '患者不在该术间，可能已被移动'

    SURGEON_ALREADY_DELETED = '术者已被其他人删除'

    ASSISTANT_ALREADY_DELETED = '一助已被其他人删除'

    ROOM_BLOCKING = '术间正在排序, 请稍候'
    ROOM_SORTING_TIMEOUT = '长时间未操作，刷新页面'

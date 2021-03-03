import win32pdh


def get_processes():
    win32pdh.EnumObjects(None, None, win32pdh.PERF_DETAIL_WIZARD)
    # instances  是所有的进程名称
    junk, instances = win32pdh.EnumObjectItems(None, None, 'Process', win32pdh.PERF_DETAIL_WIZARD)

    proc_dict = {}
    # 建立进程状态字典并更新进程状态
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance] = 0

    proc_ids = []
    for instance, max_instances in proc_dict.items():
        for inum in range(max_instances + 1):
            hq = win32pdh.OpenQuery()  # initializes the query handle
            print(hq)
            try:
                # 查找出进程句柄位置
                path = win32pdh.MakeCounterPath((None, 'Process', instance, None, inum, 'ID Process'))

                counter_handle = win32pdh.AddCounter(hq, path)  # convert counter path to counter handle
                info = win32pdh.GetCounterInfo(counter_handle, 3)
                print(info)
                try:
                    win32pdh.CollectQueryData(hq)  # collects data for the counter
                    # val为进程id
                    type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
                    print(val)
                    proc_ids.append((instance, val))
                except Exception as e:
                    print(repr(e))
                    pass
                win32pdh.RemoveCounter(counter_handle)

            except Exception as e:
                print(repr(e))
                pass
            win32pdh.CloseQuery(hq)
    return proc_ids


if __name__ == "__main__":
    get_processes()

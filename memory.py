#5.内存总量/Gb
def get_memory_info(ssh):
    """get memory sum size"""
    cmd04='wmic memorychip get capacity'
    retry_number1=3
    try:
        while True:
            if retry_number1 == 0:
                logger.writeLog("get memory sum size fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd04)
            data04=stdout.read().decode().strip('Capacity')
            print(data04)
            if data04 == "":
                retry_number1 -= 1
                logger.writeLog("get memory sum size data null",level='error')
                continue
            else:
                result_list=data04.split()
                print(result_list)
                memory_size=float(int(result_list[0])+int(result_list[1]))/1024/1024/1024
                print("mem total Gb: ",memory_size)
                logger.writeLog("get memory sum size success",level='info')
                # return memory_size
                break
    except:
        logger.writeLog("get memory size error",level='error')
        return None

#6.内存剩余量/Gb
# def get_memory_surplus(ssh):
    """get memory surplus"""
    cmd05='wmic OS get FreePhysicalMemory'
    retry_number2=3
    try:
        while True:
            if retry_number2 == 0:
                logger.writeLog("get memory surplus fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd05)
            data05=int(stdout.read().decode().split()[1])
            print(data05)
            if data05 == "":
                logger.writeLog("get memory surplus data null",level='error')
                retry_number2 -= 1
                continue
            else:
                memory_surplus=round(float(data05)/1024/1024,4)
                print("mem free Gb: ",memory_surplus)
                logger.writeLog("get memory surplus data success",level='info')
                # return memory_surplus
                break
    except:
        logger.writeLog("get memory surplus error",level='error')
        return None

#7.内存使用率
# def get_memory_ratio(ssh):
    """get memory ratio"""
    # memory_size=get_memory_size(ssh)
    # memory_surplus=get_memory_surplus(ssh)
    if memory_size == "" or memory_surplus == "":
        logger.writeLog("memory_szie is null or memory_surplus is null",level='error')
        return None
    else:
        try:
            data06=round(float((memory_size-memory_surplus))/memory_size,4)
            print("mem use ratio: ",data06)
            logger.writeLog("get memory ratio success",level='info')
            return (memory_size,memory_surplus,data06)
        except:
            logger.writeLog("get memory ratio error",level='error')
            return None
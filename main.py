from Change.Check import Checks

physicalMemory = {}
tlb = []
pageTable = []
pageFaultCounter = 0
tlbHitCounter = 0
addressReadCounter = 0


def main_func():
    global physicalMemory
    global tlb
    global pageTable
    global pageFaultCounter
    global tlbHitCounter
    global addressReadCounter

    outputFile = open('../output.txt', 'w')
    with open('addresses.txt', 'r') as addressFile:
        for line in addressFile:
            tlbHit = 0
            pageTableTrue = 0
            logicalAddress = int(line)
            offset = logicalAddress & 255
            pageOriginal = logicalAddress & 65280
            page_number = pageOriginal >> 8
            addressReadCounter += 1

            print(f"Logical address is: {logicalAddress} PageNumber is: {page_number} Offset: {offset}")
            obj = Checks(page_number, physicalMemory, offset, logicalAddress, tlb, addressReadCounter, outputFile)
            tlbHit = obj.check_tlb()

            if tlbHit:
                tlbHitCounter += 1

            if not tlbHit:
                pageTableTrue = obj.check_page_table(pageTable)

            if pageTableTrue is False and tlbHit is False:
                print("This is a page fault!")
                Checks.page_fault_handler(page_number, tlb, pageTable, physicalMemory)
                pageFaultCounter += 1
                obj.check_tlb()

    pageFaultRate = pageFaultCounter / addressReadCounter
    tlbHitRate = tlbHitCounter / addressReadCounter
    outStr = 'Number of translated address: ' + str(addressReadCounter) + '\n' + 'Number of page fault: ' + str(
        pageFaultCounter) + '\n' + 'Page fault rate: ' + str(pageFaultRate) + '\n' + 'Number of TLB hits: ' + str(
        tlbHitCounter) + '\n' + 'TLB hit rate: ' + str(tlbHitRate) + '\n'
    print(outStr)
    outputFile.write(outStr)
    outputFile.close()
    addressFile.close()


if __name__ == '__main__':
    main_func()

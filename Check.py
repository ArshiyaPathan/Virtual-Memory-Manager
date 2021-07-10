class Checks:
    def __init__(self, Page_Number, physical_Memory, Offset, logical_Address, tlb, i, Output_File):
        self.Page_Number = Page_Number
        self.physical_Memory = physical_Memory
        self.Offset = Offset
        self.logical_Address = logical_Address
        self.tlb = tlb
        self.i = i
        self.Output_File = Output_File

    @staticmethod
    def update_TLB(pageNumber, frameNumber, tlb):
        if len(tlb) < 16:
            tlb.append([pageNumber, frameNumber])
        else:
            tlb.pop(0)
            tlb.append([pageNumber, frameNumber])
        print(f"Successfully update TLB with pageNumber: {pageNumber} frameNumber: {frameNumber} !")

    @staticmethod
    def update_page_table(pageNumber, frameNumber, pageTable):
        if len(pageTable) < 256:
            pageTable.append([pageNumber, frameNumber])
        else:
            pageTable.pop(0)
            pageTable.append([pageNumber, frameNumber])
        print(f'Successfully update pageTable table with pageNumber: {pageNumber} frameNumber: {frameNumber}!')

    @staticmethod
    def update_TLB_counter(latestEntryIndex, tlb):
        latestEntry = tlb[latestEntryIndex]
        tlb.pop(latestEntryIndex)
        tlb.append(latestEntry)
        print('Successfully update TLB with new sequence using LRU!')

    @staticmethod
    def update_page_table_counter(latestEntryIndex, pageTable):
        latestEntry = pageTable[latestEntryIndex]
        pageTable.pop(latestEntryIndex)
        pageTable.append(latestEntry)
        print('Successfully update page table with new sequence using LRU!')

    @staticmethod
    def read_physical_memory(frameNumber, offset, physicalMemory):
        if (int(frameNumber) < 256) and (int(offset) < 256):
            data = physicalMemory[int(frameNumber)][int(offset)]
            print(f""" Successfully read frameNumber: \" {frameNumber} \" Offset: \" {offset} \"s data: {data} in the 
            physical memory! \n""")
            return data
        else:
            print('Frame number or offset is out of bound')

    @staticmethod
    def page_fault_handler(pageNumber, tlb, pageTable, physicalMemory):
        if int(pageNumber) < 256:
            for i in range(256):
                if i in physicalMemory.keys():
                    continue
                else:
                    frameNumber = str(i)
                    break
            backStore = open("BACKING_STORE.bin", "rb")
            physicalMemory[int(frameNumber)] = []
            for i in range(256):
                backStore.seek(int(pageNumber) * 256 + i)
                data = str(int.from_bytes(backStore.read(1), byteorder='big', signed=True))
                physicalMemory[int(frameNumber)].insert(i, data)
            backStore.close()
            print(f""" Found page \"  {pageNumber}  \" has data: {physicalMemory[int(frameNumber)]} in the backing 
            store!\n """)
        else:
            print(f'Page \" {pageNumber} \" is out of bound!')
            return
        Checks.update_TLB(pageNumber, frameNumber, tlb)
        Checks.update_page_table(pageNumber, frameNumber, pageTable)

    def check_tlb(self) -> bool:
        for j in range(len(self.tlb)):
            if self.Page_Number == self.tlb[j][0]:
                print(f"Page Number \" {str(self.Page_Number)} \" found in TLB!")
                frameNumber = self.tlb[j][1]
                data = Checks.read_physical_memory(frameNumber, self.Offset, self.physical_Memory)
                physicalAddress = "{0:08b}".format(int(frameNumber)) + "{0:08b}".format(self.Offset)
                physicalAddress = int(physicalAddress, 2)
                outStr = f"{self.i} Virtual address: {self.logical_Address} Physical address: {physicalAddress} Value: {data} \n"
                print(outStr)
                self.Output_File.write(outStr)
                Checks.update_TLB_counter(j, self.tlb)
                return True
        return False

    def check_page_table(self, pageTable) -> bool:
        for k in range(len(pageTable)):
            if self.Page_Number == pageTable[k][0]:
                print(f"Page Number \" {self.Page_Number} \" found in page table!!")
                frameNumber = pageTable[k][1]
                data = Checks.read_physical_memory(frameNumber, self.Offset, self.physical_Memory)
                physicalAddress = "{0:08b}".format(int(frameNumber)) + "{0:08b}".format(self.Offset)
                physicalAddress = int(physicalAddress, 2)
                outStr = f'{self.i} Virtual address: {self.logical_Address} Physical address: {physicalAddress} value: {data} \n'
                print(outStr)
                self.Output_File.write(outStr)
                Checks.update_page_table_counter(k, pageTable)
                return True
        return False

import xlrd
import quote
import cPickle

if __name__ == '__main__':
    with open("quotes.dat", 'r') as qf:
        quotes = cPickle.load(qf)

    with open("topics.dat", 'r') as tf:
        quote.Topic.topics = cPickle.load(tf)

    # for q in quotes:
    #     q.firsttime = None
    #     q.itemreq = None
    #
    # with open("quotes.dat", 'w') as qf:
    #     cPickle.dump(quotes, qf)

    # with xlrd.open_workbook("C:\Temp\MWD.xlsx") as book:
    #     sheet = book.sheet_by_index(1)
    #     for i in range(1, sheet.nrows - 1):
    #         row = sheet.row(i)
    #         q = quote.Quote()
    #         topic = sheet.cell_value(i, 0)
    #         if topic not in quote.Topic.topics:
    #             quote.Topic.topics.append(quote.Topic(topic))
    #         q.topic = topic
    #         q.speaker = sheet.cell_value(i, 1)
    #         q.dial = sheet.cell_value(i, 2)
    #         q.result = sheet.cell_value(i, 3)
    #         q.race = sheet.cell_value(i, 4)
    #         q.class_ = sheet.cell_value(i, 5)
    #         q.gender = sheet.cell_value(i, 6)
    #         q.cell = sheet.cell_value(i, 7)
    #         q.faction = sheet.cell_value(i, 8)
    #         q.rank = sheet.cell_value(i, 9)
    #         q.pcfaction = sheet.cell_value(i, 10)
    #         q.pcrank = sheet.cell_value(i, 11)
    #         q.mindisp = sheet.cell_value(i, 12)
    #         q.var1 = sheet.cell_value(i, 13)
    #         q.var2 = sheet.cell_value(i, 14)
    #         q.var3 = sheet.cell_value(i, 15)
    #         q.var4 = sheet.cell_value(i, 16)
    #         q.var5 = sheet.cell_value(i, 17)
    #         q.var6 = sheet.cell_value(i, 18)
    #         q.sharedby = sheet.cell_value(i, 19)
    #
    #         quotes.append(q)
    #
    #
    #     with open("C:\Temp\\topics.dat", 'w') as tf:
    #         cPickle.dump(quote.Topic.topics, tf)

    #with quote.Topic.topics[19] as topic:

    numwords = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
    cat = """
Morrowind:Enar Releth
    """
    headers = []
    for line in cat.splitlines():
        if line.find(":") > 1:
            headers.append(line[line.index(":")+1:])
    for header in headers:
        results = []
        rtopics = []
        last = -1
        print "\n" + header + "\n==Dialogue=="
        for q in quotes:
            if q.speaker.lower() == header.lower():
                if q.topic.startswith("Greeting"):
                    q.topic = "Greeting"
                results.append(q)
                if q.topic not in rtopics:
                    if q.topic == "Greeting":  # Make sure Greetings are first to be printed
                        rtopics.insert(0, q.topic)
                    else:
                        rtopics.append(q.topic)

        for t in rtopics:
            tquotes = [result for result in results if result.topic == t]
            print '*\'\'\'' + t + '\'\'\':'
            for r1 in tquotes:
                r1.processvars()
            if len(tquotes) == 1:
                onlyq = tquotes[0]
                onlyq.lineconditions()
                print onlyq.tablerow("personcont")
            else:
                for r2 in tquotes:
                    if r2.callschoices:
                        r2.lineconditions()
                        print r2.tablerow("personcont")
                        for i, cnum in enumerate(r2.callschoices):
                            responses = []
                            for r3 in tquotes:
                                if r3.choicenum == cnum:
                                    responses.append(r3)

                            if not responses:
                                print '::\'\'\'' + r2.choicestext[i] + '\'\'\''
                            if len(responses) == 1:
                                print '::\'\'\'' + r2.choicestext[i] + ':\'\'\' ' + responses[0].tablerow("response")
                            else:
                                print '::\'\'\'' + r2.choicestext[i] + ':\'\'\''
                                for response in responses:
                                    print ':::' + response.tablerow("response")
                    elif r2.choicenum:
                        continue
                    else:
                        r2.lineconditions()
                        print r2.tablerow("personcont")

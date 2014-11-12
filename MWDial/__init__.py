import quote
from quote import Topic
import cPickle

numwords = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}

if __name__ == '__main__':
    with open("quotes.dat", 'r') as qf:
        quotes = cPickle.load(qf)

    with open("topics.dat", 'r') as tf:
        Topic.topics = cPickle.load(tf)

    # for q in quotes:
    #     q.firsttime = None
    #     q.itemreq = None
    #
    # with open("quotes.dat", 'w') as qf:
    #     cPickle.dump(quotes, qf)

    pagenames = """
Morrowind:Eleedal_Lei
    """
    searchterms = []
    for line in pagenames.splitlines():
        if line.find(":") > 1:
            searchterms.append(line[line.index(":")+1:])
        else:
            searchterms.append(line)
    for term in searchterms:
        results = []
        rtopics = []
        last = -1
        print "\n" + term + "\n==Dialogue=="
        for q in quotes:
            if q.speaker.lower() == term.lower():
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

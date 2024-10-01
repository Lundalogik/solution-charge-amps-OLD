dsl = """
company:
    _label: company
    name:
        type: string
        label: name
        required: true
        length: 200
    phone:
        type: phone
        label: businesstelephonenumber
        required: false
        length: 32
    www:
        type: link
        label: businesshomepage
        required: false
        length: 100
    postaladdress1:
        type: string
        label: streetaddress
        required: false
        length: 72
    visitingaddress1:
        type: string
        label: visitingaddress-streetaddress
        required: false
        length: 72
    registrationno:
        type: string
        label: companynumber
        required: false
        length: 16
    document:
        type: hasmany
        related: document
        backref: company
    person:
        type: hasmany
        related: person
        backref: company
    coworker:
        type: belongsto
        related: coworker
        backref: company
        label: responsiblecoworker
    postalzipcode:
        type: string
        label: zipcode
        required: false
        length: 10
    postalcity:
        type: string
        label: city
        required: false
        length: 72
    visitingzipcode:
        type: string
        label: visitingaddress-zipcode
        required: false
        length: 10
    visitingcity:
        type: string
        label: visitingaddress-city
        required: false
        length: 72
    postaladdress2:
        type: string
        label: streetaddress2
        required: false
        length: 72
    visitingaddress2:
        type: string
        label: visitingaddress-streetaddress2
        required: false
        length: 72
    country:
        type: string
        label: country
        required: false
        length: 64
    buyingstatus:
        type: option
        defaultvalue: empty
        options:
            - empty
            - notinterested
            - prospect
            - active
            - excustomer
            - inactive
    deal:
        type: hasmany
        related: deal
        backref: company
    todo:
        type: hasmany
        related: todo
        backref: company
    history:
        type: hasmany
        related: history
        backref: company
    fullpostaladdress:
        type: text
        label: none
        required: false
        length: 500
    fullvisitingaddress:
        type: text
        label: businessaddress
        required: false
        length: 500
    lead:
        type: hasmany
        related: lead
        backref: company
    invoiceaddress1:
        type: string
        label: none
        required: false
        length: 72
    invoiceaddress2:
        type: string
        label: none
        required: false
        length: 72
    invoicezipcode:
        type: string
        label: none
        required: false
        length: 10
    invoicecity:
        type: string
        label: none
        required: false
        length: 72
    fullinvoiceaddress:
        type: text
        label: none
        required: false
        length: 256
    emailinvoice:
        type: link
        label: primaryemailaddress
        required: false
        length: 1073741823
    erp_id:
        type: string
        label: key
        required: false
        length: 32
    erp_status:
        type: option
        defaultvalue: empty
        options:
            - empty
            - readyforfirstsync
            - updatesmade
            - inprocess
            - synced
            - error
    erp_turnover_yearnow:
        type: decimal
        required: false
    erp_turnover_lastyeartodate:
        type: decimal
        required: false
    erp_turnover_lastyear:
        type: decimal
        required: false
    erp_salestrend:
        type: option
        defaultvalue: empty
        options:
            - empty
            - increasing
            - steady
            - decreasing
    erp_ytdgrowth:
        type: decimal
        required: false
    erp_errormessage:
        type: text
        label: none
        required: false
        length: 512
    erp_firstsynced:
        type: time
        label: none
        required: false
        defaultvalue:
    erp_lastsynced:
        type: time
        label: none
        required: false
    classification:
        type: option
        defaultvalue: empty
        options:
            - empty
            - a
            - b
            - c
    potential:
        type: option
        defaultvalue: empty
        options:
            - empty
            - one
            - two
            - three
    latestsalescontact:
        type: date
        required: false
        defaultvalue:
coworker:
    _label: coworker
    name:
        type: string
        label: name
        required: false
        length: 83
    phone:
        type: phone
        label: businesstelephonenumber
        required: false
        length: 32
    mobilephone:
        type: phone
        label: mobiletelephonenumber
        required: false
        length: 32
    email:
        type: link
        label: primaryemailaddress
        required: false
        length: 128
    username:
        type: user
    inactive:
        type: yesno
        label: inactive
    deal:
        type: hasmany
        related: deal
        backref: coworker
    company:
        type: hasmany
        related: company
        backref: coworker
    document:
        type: hasmany
        related: document
        backref: coworker
    office:
        type: belongsto
        related: office
        backref: coworker
        label: none
    todo:
        type: hasmany
        related: todo
        backref: coworker
    history:
        type: hasmany
        related: history
        backref: coworker
    picture:
        type: file
    firstname:
        type: string
        label: firstname
        required: true
        length: 32
    lastname:
        type: string
        label: lastname
        required: false
        length: 50
    lastlogintime:
        type: time
        label: none
        required: false
        defaultvalue:
    admin:
        type: yesno
        label: none
    department:
        type: option
        defaultvalue: '308501'
        options:
            - '308501'
            - sales
            - marketing
            - finance
            - administration
    lead:
        type: hasmany
        related: lead
        backref: coworker
history:
    _label: history
    date:
        type: time
        label: startdate
        required: true
        defaultvalue: getdate()
    type:
        type: option
        defaultvalue: empty
        options:
            - empty
            - talkedto
            - customervisit
            - salescall
            - noanswer
            - comment
            - sentemail
            - receivedemail
            - autolog
    note:
        type: text
        label: notes
        required: true
        length: 1073741823
    company:
        type: belongsto
        related: company
        backref: history
        label: none
    deal:
        type: belongsto
        related: deal
        backref: history
        label: none
    coworker:
        type: belongsto
        related: coworker
        backref: history
        label: responsiblecoworker
    person:
        type: belongsto
        related: person
        backref: history
        label: none
    document:
        type: belongsto
        related: document
        backref: history
        label: none
    lead:
        type: belongsto
        related: lead
        backref: history
        label: none
person:
    _label: person
    firstname:
        type: string
        label: firstname
        required: true
        length: 32
    inactive:
        type: yesno
        label: inactive
    phone:
        type: phone
        label: businesstelephonenumber
        required: false
        length: 32
    mobilephone:
        type: phone
        label: mobiletelephonenumber
        required: false
        length: 32
    email:
        type: link
        label: primaryemailaddress
        required: false
        length: 100
    deal:
        type: hasmany
        related: deal
        backref: person
    company:
        type: belongsto
        related: company
        backref: person
        label: none
    document:
        type: hasmany
        related: document
        backref: person
    lastname:
        type: string
        label: lastname
        required: false
        length: 50
    name:
        type: string
        label: name
        required: false
        length: 83
    todo:
        type: hasmany
        related: todo
        backref: person
    history:
        type: hasmany
        related: history
        backref: person
    position:
        type: string
        label: none
        required: false
        length: 32
    lead:
        type: hasmany
        related: lead
        backref: person
    expireddate:
        type: time
        label: none
        required: false
        defaultvalue:
    anonymizeddate:
        type: time
        label: none
        required: false
        defaultvalue:
    automatedflowparticipant:
        type: hasmany
        related: automatedflowparticipant
        backref: person
document:
    _label: document
    comment:
        type: string
        label: description
        required: false
        length: 256
    type:
        type: option
        defaultvalue: empty
        options:
            - empty
            - agreement
            - email
            - tender
            - other
            - picture
            - document
    document:
        type: file
    deal:
        type: belongsto
        related: deal
        backref: document
        label: none
    company:
        type: belongsto
        related: company
        backref: document
        label: none
    coworker:
        type: belongsto
        related: coworker
        backref: document
        label: responsiblecoworker
    person:
        type: belongsto
        related: person
        backref: document
        label: none
    history:
        type: hasmany
        related: history
        backref: document
    lead:
        type: belongsto
        related: lead
        backref: document
        label: none
lead:
    _label: lead
    firstname:
        type: string
        label: none
        required: false
        length: 256
    lastname:
        type: string
        label: none
        required: false
        length: 256
    companyname:
        type: string
        label: none
        required: false
        length: 256
    name:
        type: string
        label: none
        required: false
        length: 256
    email:
        type: link
        label: primaryemailaddress
        required: false
        length: 128
    phone:
        type: string
        label: businesstelephonenumber
        required: false
        length: 1073741823
    source:
        type: option
        defaultvalue: empty
        options:
            - empty
            - form
    company:
        type: belongsto
        related: company
        backref: lead
        label: none
    person:
        type: belongsto
        related: person
        backref: lead
        label: none
    deal:
        type: belongsto
        related: deal
        backref: lead
        label: none
    automatedflow:
        type: belongsto
        related: automatedflow
        backref: lead
    receiveddate:
        type: time
        label: none
        required: false
        defaultvalue: getdate()
    qualifydate:
        type: time
        label: none
        required: false
        defaultvalue:
    convertdate:
        type: time
        label: none
        required: false
        defaultvalue:
    rejectiondate:
        type: time
        label: none
        required: false
        defaultvalue:
    office:
        type: belongsto
        related: office
        backref: lead
        label: none
    option:
        type: option
        defaultvalue: '340101'
        options:
            - '339601'
            - '340101'
    description:
        type: text
        label: none
        required: false
        length: 4000
    leadstatus:
        type: option
        defaultvalue: new
        options:
            - new
            - qualify
            - convert
            - rejection
    history:
        type: hasmany
        related: history
        backref: lead
    todo:
        type: hasmany
        related: todo
        backref: lead
    document:
        type: hasmany
        related: document
        backref: lead
    coworker:
        type: belongsto
        related: coworker
        backref: lead
        label: none
    rejectionreason:
        type: option
        defaultvalue: empty
        options:
            - empty
            - baddata
            - notinterested
    automatedflowparticipant:
        type: hasmany
        related: automatedflowparticipant
        backref: lead
todo:
    _label: todo
    subject:
        type: string
        label: description
        required: false
        length: 128
    starttime:
        type: time
        label: startdate
        required: true
        defaultvalue: getdate()
    endtime:
        type: time
        label: duedate
        required: false
        defaultvalue:
    done:
        type: yesno
        label: completed
    note:
        type: text
        label: notes
        required: false
        length: 4000
    coworker:
        type: belongsto
        related: coworker
        backref: todo
        label: responsiblecoworker
    company:
        type: belongsto
        related: company
        backref: todo
        label: none
    person:
        type: belongsto
        related: person
        backref: todo
        label: name
    deal:
        type: belongsto
        related: deal
        backref: todo
        label: none
    todostatus:
        type: option
        defaultvalue: empty
        options:
            - empty
            - active
            - delayed
            - done
            - future
    deal2:
        type: hasmany
        related: deal
        backref: next_todo
    location:
        type: string
        label: location
        required: false
        length: 512
    calendarstatus:
        type: option
        defaultvalue: empty
        options:
            - empty
            - active
            - changed
            - deleted
    calendarid:
        type: string
        label: none
        required: false
        length: 1024
    lead:
        type: belongsto
        related: lead
        backref: todo
        label: none
deal:
    _label: deal
    dealstatus:
        type: option
        defaultvalue: contact
        options:
            - contact
            - requirement
            - tender
            - agreement
            - onhold
            - rejection
    value:
        type: decimal
        required: true
    quotesent:
        type: date
        required: false
        defaultvalue:
    expecteddate:
        type: month
        required: false
        defaultvalue:
    closeddate:
        type: date
        required: false
        defaultvalue:
    person:
        type: belongsto
        related: person
        backref: deal
        label: none
    document:
        type: hasmany
        related: document
        backref: deal
    coworker:
        type: belongsto
        related: coworker
        backref: deal
        label: responsiblecoworker
    wonlostreason:
        type: text
        label: none
        required: false
        length: 512
    company:
        type: belongsto
        related: company
        backref: deal
        label: none
    name:
        type: string
        label: name
        required: true
        length: 64
    history:
        type: hasmany
        related: history
        backref: deal
    todo:
        type: hasmany
        related: todo
        backref: deal
    probability:
        type: percent
        required: true
    weightedvalue:
        type: decimal
        required: true
    next_todo:
        type: belongsto
        related: todo
        backref: deal2
        label: none
    lead:
        type: hasmany
        related: lead
        backref: deal
    latestsalescontact:
        type: date
        required: false
        defaultvalue:
    source:
        type: option
        defaultvalue: empty
        options:
            - empty
            - form
    automatedflowparticipant:
        type: hasmany
        related: automatedflowparticipant
        backref: deal
office:
    _label: office
    name:
        type: string
        label: name
        required: true
        length: 32
    phone:
        type: phone
        label: businesstelephonenumber
        required: false
        length: 32
    fax:
        type: phone
        label: businessfaxnumber
        required: false
        length: 32
    www:
        type: link
        label: businesshomepage
        required: false
        length: 32
    registrationno:
        type: string
        label: companynumber
        required: false
        length: 32
    vatno:
        type: string
        label: none
        required: false
        length: 32
    pg:
        type: string
        label: none
        required: false
        length: 32
    bg:
        type: string
        label: none
        required: false
        length: 32
    misc:
        type: text
        label: none
        required: false
        length: 256
    coworker:
        type: hasmany
        related: coworker
        backref: office
    address:
        type: string
        label: streetaddress
        required: false
        length: 256
    zipcode:
        type: string
        label: zipcode
        required: false
        length: 10
    city:
        type: string
        label: city
        required: false
        length: 64
    visitingaddress1:
        type: string
        label: none
        required: false
        length: 256
    visitingzipcode:
        type: string
        label: none
        required: false
        length: 10
    visitingcity:
        type: string
        label: none
        required: false
        length: 64
    lead:
        type: hasmany
        related: lead
        backref: office
automatedflow:
    _label: automatedflow
    name:
        type: string
        required: True
    description:
        type: text
        length: 2048
    bw_automatedflowid:
        type: integer
    isrunning:
        type: yesno
    isdeleted:
        type: yesno
    automatedflowparticipant:
        type: hasmany
        related: automatedflowparticipant
        backref: automatedflow
    automatedflowfilterid:
        type: text
        length: 1024
    lead:
        type: hasmany
        related: lead
        backref: automatedflow
automatedflowparticipant:
    _label: automatedflowparticipant
    automatedflow:
        type: belongsto
        related: automatedflow
        backref: automatedflowparticipant
    person:
        type: belongsto
        related: person
        backref: automatedflowparticipant
    lead:
        type: belongsto
        related: lead
        backref: automatedflowparticipant
    deal:
        type: belongsto
        related: deal
        backref: automatedflowparticipant
    isready:
        type: yesno
    bw_validation_message:
        type: text
        length: 1024
    bw_automatedflowparticipantid:
        type: integer
    bw_status:
        type: option
        options:
            - initialize
            - inprogress
            - finished
            - cancelled
            - optout
            - failed
            - notaddedduetooptout
        defaultvalue: initialize
    bw_nextstep:
        type: text
        length: 1024
    bw_participantid:
        type: integer
        required: True
    bw_nextstep_time:
        type: time
"""

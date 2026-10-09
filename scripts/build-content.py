import json,re,random,os
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'private-materials'
OUTPUT=ROOT/'src/content/data.json'
subjects=[
 dict(id='dcit50',name='DCIT 50',subtitle='Object-Oriented Programming',icon='code',description='Explore Java classes, objects, constructors and class-level members.'),
 dict(id='gned07',name='GNED 07',subtitle='The Contemporary World',icon='globe',description='Globalization, economic structures, governance and regionalism.'),
 dict(id='gned10',name='GNED 10',subtitle='Gender and Society',icon='users',description='Gender and work, school, and media.'),
 dict(id='pathfit3',name='PATHFIT 3',subtitle='Racket Sports',icon='trophy',description='Pickleball, table tennis, and fundamental racket skills.')]
sources=[
 ('classes','dcit50','Classes and Objects Lecture','Classes and Objects Lecture.pdf',9,'pdf'),
 ('constructors','dcit50','Java Constructors Lecture','Java Constructors Lecture.pdf',14,'pdf'),
 ('static','dcit50','Static and This Keyword Lecture','Static and This Keyword Lecture.pdf',11,'pdf'),
 ('gned07','gned07','GNED 07 Midterm Reviewer','GNED 07 Midterm Reviewer.pdf',3,'docx'),
 ('gned10','gned10','GNED 10 Midterm Reviewer','GNED 10 Midterm Reviewer.pdf',2,'docx'),
 ('pickleball','pathfit3','PICKLEBALL','PICKLEBALL.pdf',62,'pptx'),
 ('tabletennis','pathfit3','TABLE TENNIS','TABLE-TENNIS_CVSUTANZA.pdf',34,'pdf'),
 ('fundamentals','pathfit3','Fundamental Skills in Racket Sports','FUNDAMENTAL-SKILLS-IN-RACKET-SPORTS.pdf',35,'pdf'),
]
sourceRecords=[dict(id=id,subjectId=sid,title=title,filename=filename,pages=count,originalType=ext,path='/materials/'+filename.replace(' ','%20')) for id,sid,title,filename,count,ext in sources]
topics=[
 ('classes-objects','dcit50','Classes & Objects','Understand blueprints, objects, fields, methods, state and behavior.','classes',[(1,9)],['A class is a blueprint or template for objects.','An object is an instance of a class.','Fields represent state; methods represent behavior.','The new keyword creates an object.']),
 ('constructors','dcit50','Java Constructors','Explore object initialization, constructors, overloading and chaining.','constructors',[(1,14)],['A constructor initializes the state of a newly created object.','Constructors share their class name and have no return type.','A compiler default constructor differs from an explicit no-argument constructor.','Constructor overloading uses different parameter lists; this(...) chains constructors.']),
 ('static-this','dcit50','Static & This Keyword','Class-level members, instance references and static initialization.','static',[(1,11)],['Static members belong to the class, rather than an individual object.','Static methods cannot directly access instance members without an object.','The this keyword refers to the current object.','Static initialization blocks execute during class initialization.']),
 ('globalization','gned07','Introduction to Globalization','Definitions and philosophical perspectives.','gned07',[(1,1)],['Globalization refers to increasing global interconnectedness and interdependence.','Hyperglobalists envision profound borderless transformation.','Skeptics emphasize nation-state continuity.','Transformationalists emphasize reconfiguration and glocalization.']),
 ('global-economy','gned07','Global Economy','Trade, finance, migration and OFW remittances.','gned07',[(1,1)],['Global value chains organize international trade.','Global finance involves capital and assets crossing borders.','OFWs are an important example of cross-border labor migration in the Philippines.']),
 ('market-integration','gned07','Market Integration','Horizontal, vertical, conglomerate and spatial market integration.','gned07',[(2,2)],['Horizontal integration involves competitors at the same production level.','Vertical integration links multiple stages of production or marketing.','Conglomerate integration combines unrelated enterprises.','Spatial integration concerns price signals across geographic regions.']),
 ('global-governance','gned07','Interstate System & Governance','Sovereignty, nationhood, international cooperation and institutions.','gned07',[(2,3)],['The Peace of Westphalia is associated with the sovereign state system.','A state has territory, population, government and sovereignty.','Governance involves IGOs, NGOs and treaties, without a single world government.']),
 ('world-regions','gned07','A World of Regions','Global divides, ASEAN and Asian regionalism.','gned07',[(3,3)],['Global North and Global South describe disparities in wealth and development.','Asian regionalism increases economic, political and cultural cooperation.','The ASEAN Way emphasizes consensus, non-interference and informality.']),
 ('gender-work','gned10','Gender and Work','Sex-typing, access and treatment discrimination, work-family balance.','gned10',[(1,1)],['Sex-typing assigns occupations by beliefs about biological sex.','Access discrimination concerns barriers to hiring.','Treatment discrimination concerns unequal compensation or promotions.','The maternal wall and unpaid domestic work affect workplace equality.']),
 ('gender-school','gned10','Gender and School','Gender socialization, teaching bias and responsive education.','gned10',[(1,2)],['Family and school are central agents of gender socialization.','Gender-responsive education should challenge stereotypes.','School policies and teacher training can counter explicit and implicit bias.']),
 ('gender-media','gned10','Gender and the Media','Representation, stereotypes and advertising in the available reviewer.','gned10',[(2,2)],['Media representation relates to equality and social justice.','Stereotypes are oversimplified beliefs about groups.','Advertising can reinforce gender stereotypes.']),
 ('pickleball','pathfit3','Pickleball','History, equipment, court, serving, scoring, strokes and grips.','pickleball',[(3,9),(11,14),(16,22),(24,28),(31,39),(41,60)],['Pickleball combines characteristics of badminton, tennis and table tennis.','The game was created in 1965 on Bainbridge Island, Washington.','The two-bounce rule and non-volley zone are central rules.','Core strokes include serving, dinking, volleys, drives and lobs.']),
 ('table-tennis','pathfit3','Table Tennis','Sport history, equipment, strokes, footwork, serving and rules.','tabletennis',[(3,7),(9,11),(13,31)],['Table tennis became an Olympic sport in 1988.','Typical equipment includes the table, paddle and ball.','Core strokes include backhand, forehand, push, block and smash.','A game generally goes to 11 with at least a two-point lead.']),
 ('racket-fundamentals','pathfit3','Fundamental Racket Skills','Ready position, grips, footwork, hand-eye coordination and strokes.','fundamentals',[(2,33)],['Ready position uses balance, bent knees and a racket held in front.','A grip should be firm without excessive tension.','Footwork helps players reach and recover from shots.','Hand-eye coordination helps control the ball or shuttle.']),
]

def pages_in(ranges):
 return [n for a,b in ranges for n in range(a,b+1)]

def clean(text):
 text=text.replace('\u2022','•').replace('\u0000','').replace('\r','')
 text=re.sub(r'\bDCIT 50\s*[–:-]\s*Object Oriented Programming\b','',text,flags=re.I)
 text=re.sub(r'\bFITT 3:\s*Physical Activities Towards Health and Fitness 1\b','',text,flags=re.I)
 text=re.sub(r'\bPATHFIT 3\b','',text,flags=re.I)
 text=re.sub(r'\n{3,}','\n\n',text)
 return text.strip()
docs={id:fitz.open(INPUT/filename) for id,_,_,filename,_,_ in sources}
topicRecords=[]
for id,sid,title,desc,src,ranges,summary in topics:
 sections=[]
 for n in pages_in(ranges):
  page=docs[src][n-1]
  raw=clean(page.get_text(sort=True))
  # Do not synthesize text where a page is image-only; viewer provides original
  if len(raw)<24: continue
  raw=raw[:2200]
  paragraphs=[a.strip() for a in raw.split('\n') if a.strip()]
  heading=paragraphs[0] if paragraphs else 'Page '+str(n)
  if len(heading)>100: heading='Page '+str(n)
  sections.append(dict(title=f'Page {n} · {heading[:65]}',body=raw,page=n,sourceId=src))
 topicRecords.append(dict(id=id,subjectId=sid,title=title,description=desc,sourceId=src,summary=summary,sections=sections,coverageNote=('The provided reviewer explicitly states the Gender and Media module is partially summarized due to incomplete original material.' if id=='gender-media' else None)))

Q=[]
def add(s,t,typ,diff,prompt,answer,wrong,source,page,exp,code=None):
 id=f'{s}-{t}-{len([x for x in Q if x["topicId"]==t])+1:03}'
 rec=dict(id=id,subjectId=s,topicId=t,conceptId=t+'-'+str(len([x for x in Q if x['topicId']==t])+1),type=typ,difficulty=diff,prompt=prompt,explanation=exp,sources=[dict(sourceId=source,page=page)],verificationStatus='verified',version=1)
 if typ in ('multiple-choice','code-analysis'):
  choices=[answer]+wrong
  if len(choices)!=4: raise ValueError(id+' must have four options')
  rand=random.Random(sum(ord(c) for c in id))
  rand.shuffle(choices)
  rec['options']=[dict(id='abcd'[i],text=x) for i,x in enumerate(choices)]
  rec['correctOptionId']='abcd'[choices.index(answer)]
 elif typ=='true-false':rec['correctBoolean']=bool(answer)
 elif typ=='identification':rec['acceptedAnswers']=answer if isinstance(answer,list) else [answer]
 if code:rec['code']=code
 Q.append(rec)
M=lambda s,t,p,a,w,src,pg,ex,d='easy':add(s,t,'multiple-choice',d,p,a,w,src,pg,ex)
T=lambda s,t,p,a,src,pg,ex,d='medium':add(s,t,'true-false',d,p,a,[],src,pg,ex)
I=lambda s,t,p,a,src,pg,ex,d='medium':add(s,t,'identification',d,p,a,[],src,pg,ex)
C=lambda t,p,a,w,pg,ex,code,d='hard',src='constructors':add('dcit50',t,'code-analysis',d,p,a,w,src,pg,ex,code)
# DCIT classes and objects
s='dcit50';t='classes-objects';src='classes'
M(s,t,'What is a class in Java?','A blueprint or template used to create objects',['An object already created in memory','An instruction that repeats code','A variable that stores only numbers'],src,1,'The lecture defines a class as a blueprint or template.')
M(s,t,'What is an object?','An instance of a class',['A blueprint for many classes','The name of a Java package','A keyword that creates a method'],src,2,'Objects are actual instances built from a class.')
I(s,t,'Which Java keyword commonly creates an object?',['new'],src,3,'The new keyword requests creation of an object.')
M(s,t,'Which best represents the state of an object?','Fields or instance variables',['Methods only','Import statements','Comments'],src,4,'Stored values make up the object state.')
M(s,t,'What represents the behavior of an object?','Methods',['Object references only','Instance fields only','The class name alone'],src,5,'Methods implement actions or operations.')
T(s,t,'Two objects created from the same class must contain identical field values.',False,src,3,'Separate objects may have independent field values.')
M(s,t,'In Student student1 = new Student(), what is student1?','A reference variable',['A constructor declaration','A static block','The class keyword'],src,4,'student1 refers to the object created by new.')
M(s,t,'What does Student() do in a new Student() expression?','Calls the constructor',['Declares a new class','Creates a for-loop','Imports a library'],src,4,'Student() invokes the class constructor.')
T(s,t,'One class can be used to create multiple separate objects.',True,src,3,'A class is a template; multiple instances can be created from it.')
I(s,t,'What is another term for an object created from a class?',['instance','an instance'],src,7,'The lecture lists instance as another term for an object.')
# constructors
s='dcit50';t='constructors';src='constructors'
M(s,t,'What is the primary purpose of a Java constructor?','Initialize an object’s state',['Run a loop forever','Delete the current class','Automatically import Java packages'],src,1,'A constructor initializes fields when an object is created.')
T(s,t,'A Java constructor must have the same name as its class.',True,src,2,'The class and constructor names must match.')
M(s,t,'What return type must a constructor declare?','No return type',['void','int','Object'],src,2,'A constructor has no return type, not even void.')
T(s,t,'Java constructors are inherited by subclasses in the same way instance methods are.',False,src,3,'The source explains that constructors are not inherited; super() may invoke a superclass constructor.')
M(s,t,'What happens if no constructor is declared in a Java class?','The compiler may provide a default no-argument constructor',['The class always fails to compile','Every field receives random values','The class becomes static'],src,3,'A compiler-provided default constructor exists when no constructor is declared.')
M(s,t,'What distinguishes a programmer-written no-argument constructor from a compiler-provided default constructor?','It is explicitly declared by the programmer',['It must accept two parameters','It cannot initialize fields','It always returns void'],src,5,'The reviewer differentiates explicit no-argument constructors and compiler defaults.')
M(s,t,'What is constructor overloading?','Multiple constructors with different parameter lists',['Using several classes with identical names','Calling a static method twice','Giving a constructor a return type'],src,8,'Overloading is determined by distinct parameter lists.')
T(s,t,'Changing only parameter names, while keeping parameter types and order, overloads a constructor.',False,src,9,'The parameter list types/order, not local names, determine overloads.')
I(s,t,'Which keyword invokes another constructor in the same class?',['this','this()'],src,10,'Constructor chaining uses this(...).')
M(s,t,'Where must a this(...) constructor call appear?','As the first statement in a constructor',['Only after a return statement','Inside a static method','Immediately after a class closes'],src,10,'The lecture specifies this(...) must be the first constructor statement.')
M(s,t,'What is the purpose of a copy constructor pattern?','Initialize an object using values from another object',['Delete an earlier object','Turn instance fields into static fields','Convert the class into an interface'],src,11,'The lecture demonstrates a Student(Student other) constructor copying state.')
C(t,'What does this Java code print?','Unknown',['null','0','Compilation error'],5,'The programmer-written no-argument constructor assigns Unknown to name.', 'class Student {\n  String name;\n  Student() { name = "Unknown"; }\n}\nSystem.out.println(new Student().name);')
C(t,'What happens when this code is compiled?','Compilation error: no matching zero-argument constructor',['Prints null','Prints Juan','Creates a default constructor automatically'],4,'Declaring Student(String) prevents Java from generating a no-argument default constructor.', 'class Student {\n  Student(String name) {}\n}\nStudent s = new Student();')
C(t,'What does this code print?','Juan',['name','null','Compilation error'],7,'this.name refers to the instance field; name refers to the parameter.', 'class Student {\n  String name;\n  Student(String name) { this.name = name; }\n}\nSystem.out.println(new Student("Juan").name);')
# static
s='dcit50';t='static-this';src='static'
M(s,t,'Which statement about a static field is correct?','It belongs to the class and is shared among instances',['Each object owns an independent static copy','It only exists inside constructors','It cannot hold a String'],src,1,'A static member belongs to the class, not to individual objects.')
M(s,t,'What is the preferred way to access a public static field?','Through the class name',['Only through this','Only inside a constructor','Only after calling super'],src,3,'The lecture prefers ClassName.field for static members.')
I(s,t,'Which Java keyword refers to the current object?',['this'],src,8,'this is a reference to the current instance.')
T(s,t,'A static method can directly access an instance variable without an object reference.',False,src,4,'A static method has no implicit instance to identify that field.')
M(s,t,'Why is Java main() declared static?','The JVM can invoke it without creating an instance first',['It ensures every variable is global','It prevents method calls','It makes methods execute twice'],src,4,'A static main method can be invoked without an instance.')
M(s,t,'What is the purpose of a static initialization block?','Perform initialization when the class is initialized',['Create a different object on every line','Pause a timer','Provide a return type for constructors'],src,6,'The lecture presents static blocks for class-level initialization.')
T(s,t,'The this keyword can be used directly inside a static method.',False,src,5,'this requires a current object; a static context has none.')
M(s,t,'Which member can a static method use directly?','Another static member of the class',['Any instance field without an object','The current object via this','All non-static methods without a receiver'],src,6,'Static methods can directly access static members.')
C(t,'What is printed by the code?','3',['0','1','Compilation error'],3,'The static counter is shared and incremented once for each object.', 'class Student {\n  static int count = 0;\n  Student() { count++; }\n}\nnew Student();\nnew Student();\nnew Student();\nSystem.out.println(Student.count);',src='static')
C(t,'What does this code print?','30',['20','10','Compilation error'],3,'Static Calculator.add(10,20) returns the sum 30.', 'class Calculator {\n  static int add(int a,int b) { return a+b; }\n}\nSystem.out.println(Calculator.add(10,20));',src='static',d='medium')
C(t,'What happens to this declaration?','Compilation error: this in static context',['Prints Juan','Creates a new object','Returns null'],5,'The keyword this cannot be referenced from static context.', 'class Student {\n  String name;\n  static void show() {\n    System.out.println(this.name);\n  }\n}',src='static')
# GNED07
s='gned07';src='gned07';t='globalization'
M(s,t,'What is globalization?','Increasing interconnectedness and interdependence across the world',['The complete separation of states','Only the movement of goods inside one city','The elimination of all cultures'],src,1,'The reviewer defines globalization as increasing worldwide interconnectedness.')
M(s,t,'Which perspective expects a single borderless world and reduced national-government power?','Hyperglobalist',['Skeptic','Transformationalist','Protectionist'],src,1,'Hyperglobalists expect a profound global transformation.')
M(s,t,'Which perspective emphasizes nation-state continuity and doubts globalization is unprecedented?','Skeptic / Anti-Globalist',['Hyperglobalist','Transformationalist','Regional federalist'],src,1,'Skeptics see globalization as a continuation of historical internationalization.')
M(s,t,'Which perspective argues states are reconfigured rather than simply disappearing?','Transformationalist',['Hyperglobalist','Skeptic','Isolationist'],src,1,'Transformationalists emphasize adaptation and glocalization.')
I(s,t,'What term refers to global forces interacting with local contexts?',['glocalization'],src,1,'The reviewer associates glocalization with the transformationalist perspective.')
T(s,t,'The globalization reviewer describes globalization as including cultural exchange.',True,src,1,'Globalization encompasses more than trade, including cultural integration.')
# global economy
s='gned07';t='global-economy';src='gned07'
M(s,t,'What does GVC stand for?','Global Value Chain',['Global Voting Council','General Value Credit','Governance Verification Charter'],src,1,'International production is organized through global value chains.')
M(s,t,'What is global finance?','Movement of money, capital and assets across borders',['Only local tax collection','School budgeting','Buying goods inside a single province'],src,1,'The reviewer defines finance as the cross-border movement of capital and assets.')
M(s,t,'Which group is highlighted as an example of Philippine cross-border labor migration?','Overseas Filipino Workers (OFWs)',['Municipal councilors','Only domestic students','Local warehouse employees'],src,1,'The reviewer highlights OFWs and their remittances.')
T(s,t,'The reviewer says OFW remittances contribute to the Philippine economy.',True,src,1,'Remittances from OFWs bolster national economic output.')
I(s,t,'What does BSP stand for?',['Bangko Sentral ng Pilipinas'],src,1,'The reviewer names Bangko Sentral ng Pilipinas in its discussion of finance.')
# integration
s='gned07';t='market-integration';src='gned07'
M(s,t,'Which integration involves acquiring competitors at the same production level?','Horizontal integration',['Vertical integration','Conglomerate integration','Spatial integration'],src,2,'Horizontal integration combines competitors at the same stage.')
M(s,t,'Which integration controls different stages of production or marketing?','Vertical integration',['Horizontal integration','Spatial integration','Non-interference'],src,2,'Vertical integration joins upstream and downstream stages.')
M(s,t,'Which integration combines unrelated enterprises to diversify risk?','Conglomerate integration',['Vertical integration','Horizontal integration','Spatial integration'],src,2,'Conglomerate integration combines unrelated lines of business.')
M(s,t,'Which type studies how efficiently prices transmit across geographic regions?','Spatial market integration',['Vertical integration','Corporate horizontal integration','Interstate integration'],src,2,'Spatial integration considers regional price signals.')
T(s,t,'A firm acquiring direct competitors is an example of vertical integration.',False,src,2,'Acquiring competitors at the same production level is horizontal integration.')
I(s,t,'What integration type combines unrelated businesses?',['conglomerate integration','conglomerate'],src,2,'The reviewer uses conglomerate for diversification across unrelated enterprises.')
# governance
s='gned07';t='global-governance';src='gned07'
M(s,t,'Which historical peace settlement is associated with the modern sovereign-state system?','Peace of Westphalia (1648)',['Treaty of Versailles (1919)','Paris Agreement','ASEAN Charter'],src,2,'The reviewer links the state system to Westphalia in 1648.')
M(s,t,'Which combination defines the reviewer’s state concept?','Territory, population, government and sovereignty',['Trade, currency, language and sport','Only a common language','A flag and national anthem only'],src,2,'The source lists these four components of a state.')
M(s,t,'Which idea best describes a nation in the reviewer?','An imagined community sharing culture and history',['An international bank','Only a legal government agency','A multinational company'],src,2,'The reviewer distinguishes nation from state by shared identity.')
M(s,t,'Which actor is listed as an intergovernmental organization?','World Trade Organization (WTO)',['A single household','A local school club','A private personal blog'],src,2,'The WTO is an example of an IGO in the reviewer.')
M(s,t,'Which is named as a binding international treaty?','Paris Agreement',['AFTA as a household rule','A local parking notice','Classroom attendance policy'],src,2,'The Paris Agreement is listed as an example of a treaty.')
T(s,t,'Contemporary global governance requires one world government to exist.',False,src,2,'The source explicitly defines it as collective management without one world government.')
I(s,t,'What maritime treaty framework is mentioned in connection with the West Philippine Sea dispute?',['UNCLOS','United Nations Convention on the Law of the Sea'],src,2,'UNCLOS is named in the discussion of sovereignty challenges.')
# world regions
s='gned07';t='world-regions';src='gned07'
M(s,t,'What does the Global North generally refer to in the reviewer?','Wealthy, industrialized and technologically advanced nations',['Only countries north of the equator','Exclusively island nations','Every state in ASEAN'],src,3,'North/South describes power and development disparities, not strictly latitude.')
M(s,t,'Which region is the Philippines categorized under in this reviewer?','Global South',['Global North','European Union','North Atlantic Treaty Organization'],src,3,'The source categorizes the Philippines in the Global South.')
M(s,t,'Which set best describes the ASEAN Way?','Non-interference, consensus and informality',['Majority rule and compulsory intervention','Single federal government','Only military cooperation'],src,3,'The reviewer highlights non-interference and consensus-based diplomacy.')
M(s,t,'What is Asian regionalism?','Increasing economic, political and sociocultural integration among Asian nations',['All countries adopting one language','A ban on regional trade','A single global parliament'],src,3,'Asian regionalism describes closer cooperation in Asia.')
T(s,t,'The Philippines was a founding member of ASEAN in 1967.',True,src,3,'The reviewer names the Philippines as a founding ASEAN member.')
I(s,t,'What regional grouping is characterized by consensus and non-interference?',['ASEAN','Association of Southeast Asian Nations'],src,3,'The ASEAN Way is based on those principles.')
# GNED10 gender work
s='gned10';t='gender-work';src='gned10'
M(s,t,'What is sex-typing?','Believing particular jobs suit men or women based on biological sex',['Comparing salary tables only','Assigning official grades to students','Choosing work hours based on age'],src,1,'The reviewer defines sex-typing as associating occupations with biological sex.')
M(s,t,'What is access discrimination?','Difficulty entering a job field because of sex',['Unequal pay after identical performance','Being late at work','Changing between departments voluntarily'],src,1,'Access discrimination concerns opportunities to enter an occupation.')
M(s,t,'What is treatment discrimination?','Unequal pay or promotion despite similar qualifications and performance',['Difficulty applying to a field at all','A legal right to paid leave','Scheduling normal employee training'],src,1,'Treatment discrimination concerns unequal treatment after hiring.')
M(s,t,'What does the maternal wall refer to?','Bias against mothers or pregnant employees in the workplace',['A physical wall in a hospital','A system for school registration','A benefit for all occupations'],src,1,'The maternal wall relates to pregnancy/motherhood stereotypes and penalties.')
M(s,t,'Which responsibility can limit women’s participation in paid work according to the reviewer?','Disproportionate unpaid domestic work',['Mandatory sports training','Owning a university','A universal ban on careers'],src,1,'The reviewer emphasizes unpaid domestic work burdens.')
T(s,t,'The reviewer says equal pay and adequate parental leave help address gender inequality at work.',True,src,1,'Work-family balance and equal opportunities support workplace equality.')
I(s,t,'What term refers to stereotypes assigning careers as “masculine” or “feminine”?',['sex-typing','sex typing'],src,1,'The reviewer names this belief sex-typing.')
# school
s='gned10';t='gender-school';src='gned10'
M(s,t,'Which two are identified as main pillars of gender socialization?','Family and school',['Only media and sports','Only the workplace and banks','Only governments and companies'],src,1,'The reviewer identifies family and school as socialization pillars.')
M(s,t,'What is gender socialization?','Learning socially expected ways of behaving and thinking by sex',['Learning only biological anatomy','A school’s exam timetable','An employment contract'],src,1,'Gender socialization transmits socially expected gender norms.')
M(s,t,'What should gender-responsive educators encourage?','Cross-gender interaction and counter-stereotypic examples',['Exclusive segregation in all classes','Ignoring gender harassment','Judging learners by stereotypes'],src,2,'The reviewer recommends egalitarian teaching and counter-stereotypic models.')
M(s,t,'What response to teacher bias does the reviewer support?','Explicit training backed by school policy',['Avoiding all teacher feedback','Separating students by sex for every activity','Removing all co-educational schools'],src,2,'Training can help educators identify explicit and implicit bias.')
T(s,t,'The reviewer recommends promoting egalitarian attitudes in co-educational schools.',True,src,2,'The source favors improving co-educational schools rather than default segregation.')
I(s,t,'What is the process by which individuals learn gender norms from society?',['gender socialization'],src,1,'The reviewer calls this gender socialization.')
# media
s='gned10';t='gender-media';src='gned10'
M(s,t,'What are gender stereotypes?','Oversimplified beliefs about people based on gender',['A guaranteed description of every individual','A legal form of school testing','Accurate individual assessments'],src,2,'The reviewer defines stereotypes as oversimplified group beliefs.')
M(s,t,'Which source of gender norms is emphasized in the reviewer?','Advertising and media',['Only weather forecasts','Only mathematical formulas','Only historical dates'],src,2,'The reviewer describes advertising and media as key sources of gender norms.')
T(s,t,'The source says children may internalize gender stereotypes early.',True,src,2,'The reviewer describes the effect of stereotypes on young children.')
M(s,t,'What is important for fair gender representation in media?','Media pluralism and editorial freedom',['Reducing all voices to a single group','Marketing stereotypes as facts','Ignoring human rights'],src,2,'The reviewer connects pluralism and editorial freedom with representation.')
I(s,t,'What term refers to oversimplified beliefs that members of a group are the same?',['stereotypes','gender stereotypes'],src,2,'The reviewer defines stereotypes in its media discussion.')
# sports pickleball
s='pathfit3';t='pickleball';src='pickleball'
M(s,t,'Where was pickleball created in 1965?','Bainbridge Island, Washington',['New York City','London, England','Tokyo, Japan'],src,5,'The slide identifies Bainbridge Island as its birthplace.')
M(s,t,'Which group founded pickleball?','Joel Pritchard, Bill Bell and Barney McCallum',['Only Serena Williams','The ITTF board','George Washington and Abraham Lincoln'],src,5,'The slide lists the sport’s three founders.')
M(s,t,'Which sports contributed elements to pickleball?','Badminton, tennis and table tennis',['Football, boxing and baseball','Golf, rowing and cricket','Swimming, cycling and football'],src,3,'The slide describes pickleball as a hybrid of these three sports.')
M(s,t,'How many players are on each side during pickleball doubles?','Two',['One','Three','Four'],src,25,'Doubles consists of two players per side.')
M(s,t,'What area is commonly called the kitchen in pickleball?','The non-volley zone',['The baseline','The middle of the net','The entire singles sideline'],src,14,'The kitchen is the non-volley zone.')
M(s,t,'In pickleball, how is a legal serve directed?','Diagonally into the appropriate service court',['Straight into the nearest sideline','To the server’s own court','Always into the kitchen'],src,16,'The serve is made diagonally crosscourt.')
M(s,t,'What does the two-bounce rule require?','The serve and return must each bounce before a volley is allowed',['Every shot must bounce twice','The server must bounce the ball twice before contact','Only the receiving team may volley'],src,17,'The first two shots must bounce on each side as described in the lecture.')
M(s,t,'What is a dink in pickleball?','A soft shot landing in or near the opponent’s non-volley zone',['A powerful overhead smash','A ball hit out of bounds','A serve struck from the opponent’s side'],src,36,'The dink is a soft, controlled shot used near the kitchen.')
M(s,t,'What is a volley?','Hitting the ball before it bounces',['Hitting only after three bounces','A shot always hit from the baseline','A throw rather than a paddle strike'],src,37,'A volley is hit before the ball lands.')
M(s,t,'What is a lob?','A high shot over an opponent’s head',['A low soft shot into the kitchen','A mandatory underhand serve','A side-to-side footwork drill'],src,38,'A lob sends the ball high and deep.')
M(s,t,'What is a groundstroke?','A stroke played after the ball bounces',['Any shot hit before the bounce','Only the opening serve','A grip holding the paddle vertically'],src,39,'Groundstrokes are made after a bounce.')
M(s,t,'What grip is also called the handshake grip?','Continental grip',['Two-handed backhand grip','Eastern backhand grip','A reverse penhold grip'],src,50,'The slide describes holding a continental grip as if shaking hands.')
I(s,t,'What is the pickleball term for the non-volley zone?',['kitchen','the kitchen'],src,14,'The court diagram calls the non-volley zone the kitchen.')
T(s,t,'Pickleball can be played indoors or outdoors.',True,src,3,'The definition mentions both locations.')
M(s,t,'Which shot is described as a faster, more powerful groundstroke?','Drive',['Dink','Soft return','Recovery step'],src,46,'The lecture contrasts the powerful drive with softer strokes.')
# table tennis
s='pathfit3';t='table-tennis';src='tabletennis'
M(s,t,'When did table tennis become an Olympic sport?','1988',['1965','2005','1920'],src,7,'The slide says table tennis became an Olympic sport in 1988.')
M(s,t,'Which international federation sets rules for table tennis competitions?','ITTF',['FIFA','FIBA','IOC exclusively'],src,7,'ITTF is identified as the sport’s international federation.')
M(s,t,'Where did the Victorian indoor parlor version of ping-pong develop?','England',['Australia','The Philippines','Canada'],src,4,'The history slide associates early indoor ping-pong with Victorian England.')
M(s,t,'What is the standard table tennis ball diameter in the lecture?','40 millimeters',['20 millimeters','60 millimeters','100 millimeters'],src,11,'The equipment slide states 40 mm.')
M(s,t,'How much does the standard table tennis ball weigh?','2.7 grams',['10 grams','1 gram','25 grams'],src,11,'The slide specifies 2.7 g.')
M(s,t,'How many points normally win a game of table tennis, with a two-point lead?','11',['5','21','30'],src,28,'The rule slide states 11 points and at least a two-point margin.')
M(s,t,'Which table tennis stroke is a powerful attacking shot?','Smash',['Push','Soft block','Ready position'],src,18,'The slide describes smash as a powerful shot.')
M(s,t,'Which stroke uses the racket to redirect a fast incoming shot with minimal swing?','Block',['Serve','Lob','Crossover step'],src,17,'Blocking is a defensive response to incoming shots.')
M(s,t,'Which stroke is described as a soft, controlled defensive return?','Push',['Smash','Overhead serve','Pivot footwork'],src,16,'The lecture introduces the push as a soft stroke.')
M(s,t,'Which is a table tennis footwork technique named in the lecture?','Pivot step',['Butterfly sprint','Marathon lap','Goalkeeper dive'],src,22,'The lecture lists pivot steps under footwork.')
M(s,t,'In singles table tennis, how many players face each other?','One player against one',['Two players against two','Three players against three','Four players against four'],src,30,'The slide distinguishes singles from doubles.')
T(s,t,'The table tennis lecture describes reaction time as an important skill.',True,src,31,'Reaction time is highlighted due to ball speed.')
I(s,t,'What is the abbreviation of the International Table Tennis Federation?',['ITTF'],src,7,'The slides use ITTF for the governing federation.')
# fundamentals
s='pathfit3';t='racket-fundamentals';src='fundamentals'
M(s,t,'What is the purpose of the ready position?','Prepare to react quickly to incoming shots',['Prevent movement during rallies','Guarantee every shot scores','Only prepare for rest breaks'],src,6,'Ready position prepares the player to respond quickly.')
M(s,t,'How should knees be positioned in the basic ready stance?','Slightly bent',['Completely locked','Kneeling on the ground','Lifted above the waist'],src,7,'The slide states knees should be slightly bent.')
M(s,t,'Where should the player hold the racket in the ready stance?','In front of the body',['Behind the back at all times','On the floor','Above the opponent’s head'],src,8,'The ready-position slide describes the racket held in front.')
M(s,t,'How tightly should a player hold the racket?','Firmly, but not excessively tight',['As tightly as possible','Without touching the handle','Only with fingertips extended'],src,11,'The slide recommends firm control without excess tension.')
M(s,t,'Which grip is often compared to holding a hammer?','Continental grip',['Two-handed backhand grip','Eastern forehand only','Penhold grip only'],src,12,'The fundamentals slide calls the continental grip the hammer grip.')
M(s,t,'What does footwork help a player do?','Reach shots on time and recover position',['Keep both feet permanently stationary','Avoid reading the ball','Replace hand-eye coordination'],src,17,'Good footwork helps reach the ball and reposition.')
M(s,t,'Which movement is explicitly listed as basic court footwork?','Split step',['Forward flip','Diving roll','Long-distance sprint only'],src,19,'Split step appears among basic court movements.')
M(s,t,'What is hand-eye coordination?','Using visual information to guide hand and racket movement',['Only memorizing court rules','Moving without watching the ball','A way to measure physical height'],src,24,'The slide defines coordination as translating visual input into controlled movement.')
M(s,t,'Which is a basic hand-eye coordination drill?','Ball toss and catch',['Only running a marathon','Standing with eyes closed for every rally','Never touching the racket'],src,25,'The material gives ball toss and catch as a coordination drill.')
M(s,t,'Which stroke uses the dominant side of the body?','Forehand',['Backhand','Recovery step','Split step'],src,27,'The forehand is performed on the dominant side.')
M(s,t,'Which stroke is performed on the non-dominant side?','Backhand',['Forehand','Volley serve','Only a dink'],src,28,'The backhand is performed on the opposite side.')
M(s,t,'Which activity practices keeping the ball bouncing on the racket?','Racket tapping',['Pivot step','Static block','The two-bounce rule'],src,30,'Racket tapping is included among ball-control activities.')
T(s,t,'A relaxed but alert posture is recommended in the ready position.',True,src,8,'The slide recommends being relaxed and alert.')
I(s,t,'What is the ability to guide hand movements using visual information called?',['hand-eye coordination','hand eye coordination'],src,24,'The source defines hand-eye coordination in this way.')

# Ensure code-analysis examples are complete Java programs, not stray top-level statements.
code_overrides={
 ('constructors', 'What does this Java code print?'): 'class Student {\n  String name;\n  Student() { name = "Unknown"; }\n}\nclass Main {\n  public static void main(String[] args) {\n    System.out.println(new Student().name);\n  }\n}',
 ('constructors', 'What happens when this code is compiled?'): 'class Student {\n  Student(String name) {}\n}\nclass Main {\n  public static void main(String[] args) {\n    Student s = new Student();\n  }\n}',
 ('constructors', 'What does this code print?'): 'class Student {\n  String name;\n  Student(String name) { this.name = name; }\n}\nclass Main {\n  public static void main(String[] args) {\n    System.out.println(new Student("Juan").name);\n  }\n}',
 ('static-this','What is printed by the code?'): 'class Student {\n  static int count = 0;\n  Student() { count++; }\n}\nclass Main {\n  public static void main(String[] args) {\n    new Student();\n    new Student();\n    new Student();\n    System.out.println(Student.count);\n  }\n}',
 ('static-this','What does this code print?'): 'class Calculator {\n  static int add(int a,int b) { return a+b; }\n}\nclass Main {\n  public static void main(String[] args) {\n    System.out.println(Calculator.add(10,20));\n  }\n}',
}
for q in Q:
 key=(q['topicId'],q['prompt'])
 if key in code_overrides:q['code']=code_overrides[key]

# quality checks
ids=[q['id'] for q in Q]
assert len(ids)==len(set(ids)), 'duplicate ids'
for q in Q:
 assert q['explanation'] and q['sources'][0]['page']>0
 assert q['sources'][0]['sourceId'] in docs
 assert q['topicId'] in [t['id'] for t in topicRecords]
 if q['type'] in ('multiple-choice','code-analysis'):
  assert len(q['options'])==4
  assert q['correctOptionId'] in [o['id'] for o in q['options']]
 if q['type']=='identification':assert q['acceptedAnswers']

# flashcards: sourced, traceable prompts, distinct from Q where possible
cards=[]
summary_citation_pages={
 'classes-objects':[1,2,5,3],'constructors':[1,2,5,10],'static-this':[1,4,8,6],
 'globalization':[1,1,1,1],'global-economy':[1,1,1],
 'market-integration':[2,2,2,2],'global-governance':[2,2,2],
 'world-regions':[3,3,3],'gender-work':[1,1,1,1],
 'gender-school':[1,2,2],'gender-media':[2,2,2],
 'pickleball':[3,5,17,36],'table-tennis':[7,9,14,28],
 'racket-fundamentals':[7,11,17,24]
}
for topic in topicRecords:
 for i,point in enumerate(topic['summary']):
  cards.append(dict(id=f"{topic['id']}-card-{i+1}",subjectId=topic['subjectId'],topicId=topic['id'],front=['Key idea '+str(i+1)+': '+topic['title'],'Recall: '+topic['title'],'Explain this concept: '+topic['title'],'What should you remember about '+topic['title']+'?'][i%4],back=point,sourceId=topic['sourceId'],page=summary_citation_pages[topic['id']][i]))
# include Q-based cards for more coverage, avoid code snippets
for q in Q:
 if q['type']=='code-analysis':continue
 answer=next((o['text'] for o in q.get('options',[]) if o['id']==q.get('correctOptionId')),None)
 if q['type']=='identification':answer=q['acceptedAnswers'][0]
 if q['type']=='true-false':answer=('True' if q['correctBoolean'] else 'False')+' — '+q['explanation']
 cards.append(dict(id=q['id']+'-card',subjectId=q['subjectId'],topicId=q['topicId'],front=q['prompt'],back=answer or '',sourceId=q['sources'][0]['sourceId'],page=q['sources'][0]['page']))

asset=dict(subjects=subjects,sources=sourceRecords,topics=topicRecords,questions=Q,flashcards=cards)
OUTPUT.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8')
from collections import Counter
print('Output',OUTPUT,'questions:',len(Q),'flashcards:',len(cards),'topics:',len(topicRecords),'lesson sections:',sum(len(t['sections']) for t in topicRecords))
print('Questions by subject',dict(Counter(q['subjectId'] for q in Q)))
print('Question formats',dict(Counter(q['type'] for q in Q)))
print('Content size KB',round(OUTPUT.stat().st_size/1024))

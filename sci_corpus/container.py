import os
import json
import codecs
import sqlite3
import xml.etree.ElementTree as ET

class ContainerDB():
    """
    Class container.
    """
    def __init__(self):
        self.__path = '../test'
        self.__isModified = False
        self.__dict = {"Not Classified":{"Not Classified":{"Not Classified":[("Sentence","Reference"),("Oi tuto pbom", "Monique")]}}}
        self.__db = sqlite3.connect('CORPUS.db')
        
        cur = self.__db.cursor()
        
        #Need to add an option to create a table!
        
        #cur.execute('''DROP TABLE corpus''')
        cur.execute('''CREATE TABLE IF NOT EXISTS
                     corpus(id INTEGER PRIMARY KEY, sec TEXT, subsec TEXT,
                     func TEXT, phrase TEXT, ref TEXT)''')
        cur.execute('''INSERT INTO corpus(sec,subsec,func,phrase,ref) VALUES(?,?,?,?,?)''',('Not Classified','Not Classified','Not Classified','This is an exemple.','journal_volume_page'))
        self.__db.commit()
        print('Connected to the database!\n')
        
    
    def addDB(self,sect=['Not Classified'],subsect=['Not Classified'],funct=['Not Classified'],phrase=['NULL'],ref=['NULL']):
        
        cursor = self.__db.cursor()
        
        whatadd = [(a,b,c,d,e) for a in sect for b in subsect for c in funct for d in phrase for e in ref]

        cursor.executemany('''INSERT INTO corpus(sec,subsec,func,phrase,ref) VALUES(?,?,?,?,?)''',whatadd)
                
        self.__db.commit()
        self.isModified  = True
    
    
    def listCategories(self,section=[],subsection=[],function=[]):
        
        cursor = self.__db.cursor()
        
        sections = []
        subsections = []
        functions = []
        
        if section == [] and subsection == [] and function == []:
           cursor.execute('''SELECT DISTINCT sec FROM corpus''')
           sections = cursor.fetchall()
                
        if section != [] and subsection == [] and function == []:
           cursor.execute('SELECT DISTINCT subsec FROM corpus WHERE sec in ({0})'.format(','.join('?' for _ in section)), section)
           subsections = cursor.fetchall()
              
        if section != [] and subsection != [] and function == []:
           secsubsecTuple = [(a,b) for a in section for b in subsection]
           for i in range(len(secsubsecTuple)):
              cursor.execute('''SELECT DISTINCT func FROM corpus WHERE sec=? AND subsec=?''',secsubsecTuple[i])
              functions.append(cursor.fetchall())
        
        sectionsFinal = []
        subsectionsFinal = []
        functionsFinal = []
        
        for i in sections:
           sectionsFinal.append(i[0])
        
        for i in subsections:
           subsectionsFinal.append(i[0])
           
        for j in functions:
           for i in range(len(j)):
              functionsFinal.append(j[i][0])

        sectionsFinal = list(set(sectionsFinal))
        subsectionsFinal = list(set(subsectionsFinal))
        functionsFinal = list(set(functionsFinal))

        return [sectionsFinal,subsectionsFinal,functionsFinal]


    def listSentences(self,section=[],subsection=[],function=[]):

        cursor = self.__db.cursor()
        
        phrases = []

        if section == [] and subsection == [] and function == []:
           cursor.execute('''SELECT DISTINCT phrase, ref FROM corpus''')
           phrases.append(cursor.fetchall())
        
        if section != [] and subsection == [] and function == []:
           cursor.execute('SELECT DISTINCT phrase, ref FROM corpus WHERE sec in ({0})'.format(','.join('?' for _ in section)), section)
           phrases.append(cursor.fetchall())
        
        if section != [] and subsection != [] and function == []:
           secsubsecTuple = [(a,b) for a in section for b in subsection]
           for i in range(len(secsubsecTuple)):
              cursor.execute('''SELECT DISTINCT phrase, ref FROM corpus WHERE sec=? AND subsec=?''',secsubsecTuple[i])
              phrases.append(cursor.fetchall())
        
        if section != [] and subsection != [] and function != []:
           secsubsecfuncTuple = [(a,b,c) for a in section for b in subsection for c in function]
           for i in range(len(secsubsecfuncTuple)):
              cursor.execute('''SELECT DISTINCT phrase, ref FROM corpus WHERE sec=? AND subsec=? AND func=?''',secsubsecfuncTuple[i])
              phrases.append(cursor.fetchall())
                
        return phrases
        
        
    def remove(sect=[],subsect=[],funct=[],phrase=[]):

        cursor = self.__db.cursor()
        
        #whatrm = [(a,b,c,d) for a in section for b in subsection for c in function for d in phrase]
        
        if sect != [] and subsect == [] and funct == [] and phrase == []:
           whatrm = [(a,) for a in sect]
           whatup = [('Not Classified',a) for a in sect]
           cursor.executemany('DELETE FROM corpus WHERE sec=?',whatrm)
           update(section=whatup)
        
        if sect == [] and subsect != [] and funct == [] and phrase == []:
           whatrm = [(a,) for a in subsect]
           whatup = [('Not Classified',a) for a in subsect]
           cursor.executemany('DELETE FROM corpus WHERE subsec=?',whatrm)
           update(subsection=whatup)
           
        if sect == [] and subsect == [] and funct != [] and phrase == []:
           whatrm = [(a,) for a in funct]
           whatup = [('Not Classified',a) for a in funct]
           cursor.executemany('DELETE FROM corpus WHERE subsec=?',whatrm)
           update(function=whatup)
           
        if sect == [] and subsect == [] and funct == [] and phrase != []:
           whatrm = [(a,) for a in phrase]
           whatup = [('Not Classified',a) for a in phrase]
           cursor.executemany('DELETE FROM corpus WHERE subsec=?',whatrm)
           update(phrase=whatup)
             
        self.__db.commit()
        self.isModified  = True

    def update(self, section=[('NULL','NULL')],subsection=[('NULL','NULL')],function=[('NULL','NULL')],phrase=[('NULL','NULL')],ref=[('NULL','NULL')]):
        
        cursor = self.__db.cursor()

        if section != [('NULL','NULL')] and subsection == [('NULL','NULL')] and function == [('NULL','NULL')] and phrase == [('NULL','NULL')] and ref == [('NULL','NULL')]:
           cursor.execute('''UPDATE corpus 
                          SET sec=? WHERE sec=?''',section[0])
        
        if section == [('NULL','NULL')] and subsection != [('NULL','NULL')] and function == [('NULL','NULL')] and phrase == [('NULL','NULL')] and ref == [('NULL','NULL')]:
           cursor.execute('''UPDATE corpus 
                          SET subsec=? WHERE subsec=?''',subsection[0])        

        if section == [('NULL','NULL')] and subsection == [('NULL','NULL')] and function != [('NULL','NULL')] and phrase == [('NULL','NULL')] and ref == [('NULL','NULL')]:
           cursor.execute('''UPDATE corpus 
                          SET function=? WHERE function=?''',function[0]) 

        if section == [('NULL','NULL')] and subsection == [('NULL','NULL')] and function == [('NULL','NULL')] and phrase != [('NULL','NULL')] and ref == [('NULL','NULL')]:
           cursor.execute('''UPDATE corpus 
                          SET phrase=? WHERE phrase=?''',phrase[0]) 
        
        if section == [('NULL','NULL')] and subsection == [('NULL','NULL')] and function == [('NULL','NULL')] and phrase == [('NULL','NULL')] and ref != [('NULL','NULL')]:
           cursor.execute('''UPDATE corpus 
                          SET ref=? WHERE ref=?''',ref[0]) 
        
        self.__db.commit()
        self.isModified  = True  

'''
    def bulk_add(db,filename):
            
        cursor = db.cursor()
        
        tree = ET.parse(filename)      
        root = tree.getroot()
        
        info = [(w.find('PHRASE').text, w.find('FUNCTION').text, w.find('REF').text) for w in root.findall('INFOPIECE')]
        
        cursor.executemany('INSERT INTO CORPUS(phrase, function, ref) VALUES(?,?,?)',info)
        
        db.commit()
'''        
    
    @property
    def path(self):
        """
        Filepath to read and write.
        """
        return self.__path
        
    @path.setter
    def path(self, path):
        self.__path = os.path.abspath(path)
        
    @property
    def isModified(self):
        """
        Shows the answer for is modified question.
        """
        return self.__isModified
        
    @isModified.setter
    def isModified(self, state):
        self.__isModified = state
        
    def write_(self, path=''):
        """
        Writes file in path or in self.path if not passed.
        """
        if path == '':
            path = self.path
        else:
            self.path = path
        self.export_(path)
        self.isModified = False
        
    def read_(self,  path):
        """
        Reads file.
        """
        self.import_(path)
        self.path = path
        self.isModified = False
        
    def clear_(self):
        """
        Clear all fields.
        """
        self.__path = ''
        self.__isModified = False
        self.__dict = {'Not Classified':{'Not Classified':{'Not Classified':('Sentence','Reference')}}}
        
    def import_(self,  path=''):
        """
        Import file as XML, JSON, DB.
        """
        print path
        with codecs.open(path, 'rb', 'utf-8') as fp:
            text = fp.read()
            self.__dict = json.loads(str(text))
        self.isModified = False
        
    def export_(self,  path=''):
        """
        Export file as XML, JSON, DB.
        """
        print path
        with codecs.open(path, 'wb',  'utf-8') as project_file:
            json.dump(self.__dict, project_file,  indent=4,  sort_keys=True)
        self.isModified = False

class Container():
    """
    Class container.
    """
    def __init__(self):
        self.__path = '../test'
        self.__isModified = False
        self.__dict = {"Not Classified":{"Not Classified":{"Not Classified":[("Sentence","Reference"),("Oi tuto pbom", "Monique")]}}}

    def listCategoriesFromDB(self):
        """
        Do the deep update from db for categories Section, Sub Section and Function.
        We use this just with a insertion, remove or update in any category.
        """
        
    def listSentencesFromDB(self, sections=[],  sub_sections=[],  functions=[]):
        """
        Do the deep update from db for Sentences. [((Section, SubSection, Function),Sentence), ((),)]
        We use this just with a insertion, remove or update in sentence.
        """
        
    def add(self, section='Not Classified', sub_section='Not Classified', function='Not Classified', sentence='', reference=''):
        """
        
        """
        try:
            self.__dict[section]
        except KeyError:
            print 'Add section: ', section
            self.__dict[section] = {}
        finally:
            try:
                self.__dict[section][sub_section]
            except KeyError:
                print 'Add sub section: ', sub_section
                self.__dict[section][sub_section] = {}
            finally:
                try:
                    self.__dict[section][sub_section][function]
                except KeyError:
                    print 'Add function: ', function
                    self.__dict[section][sub_section][function] = []
                finally:
                    if sentence != '':
                        self.__dict[section][sub_section][function].append((sentence, reference))
                        print self.__dict[section][sub_section][function]
        self.isModified  = True
        
        
    def sections(self):
        """
        Return sections.
        """
        sections = self.__dict.keys()
        print 'sections: ',  sections
        return sections
            
        
    def subSections(self,  sections=[]):
        """
        Return sub sections from sections.
        """
        sub_sections = []
        for section in sections:
            sub_sections.extend(self.__dict[section].keys())
        #print 'sub sections: ',  sub_sections
        return sub_sections
        
    def functions(self, sections=[],  sub_sections=[]):
        """
        Return functions from sub sections.
        """
        functions = []
        for section in sections:
            for sub_section in sub_sections:
                functions.extend(self.__dict[section][sub_section].keys())
        #print 'functions: ',  functions
        return functions
        
    def sentences(self,  sections=[],  sub_sections=[],  functions=[]):
        """
        Return sentences from sections, sub_sections and functions.
        """
        sentences = []
        for section in sections:
            for sub_section in sub_sections:
                for function in functions:
                    sentences.extend(self.__dict[section][sub_section][function])
        #print 'sentences: ',  sentences
        return sentences
    
    @property
    def path(self):
        """
        Filepath to read and write.
        """
        return self.__path
        
    @path.setter
    def path(self, path):
        self.__path = os.path.abspath(path)
        
    @property
    def isModified(self):
        """
        Shows the answer for is modified question.
        """
        return self.__isModified
        
    @isModified.setter
    def isModified(self, state):
        self.__isModified = state
        
    def write_(self, path=''):
        """
        Writes file in path or in self.path if not passed.
        """
        if path == '':
            path = self.path
        else:
            self.path = path
        self.export_(path)
        self.isModified = False
        
    def read_(self,  path):
        """
        Reads file.
        """
        self.import_(path)
        self.path = path
        self.isModified = False
        
    def clear_(self):
        """
        Clear all fields.
        """
        self.__path = ''
        self.__isModified = False
        self.__dict = {'Not Classified':{'Not Classified':{'Not Classified':('Sentence','Reference')}}}
        
    def import_(self,  path=''):
        """
        Import file as XML, JSON, DB.
        """
        print path
        with codecs.open(path, 'rb', 'utf-8') as fp:
            text = fp.read()
            self.__dict = json.loads(str(text))
        self.isModified = False
        
    def export_(self,  path=''):
        """
        Export file as XML, JSON, DB.
        """
        print path
        with codecs.open(path, 'wb',  'utf-8') as project_file:
            json.dump(self.__dict, project_file,  indent=4,  sort_keys=True)
        self.isModified = False
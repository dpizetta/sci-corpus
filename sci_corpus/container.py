import os
#import json
import codecs
import sqlite3
import xml.etree.ElementTree as ET

class ContainerDB():
    """
    Class container.
    """
    def __init__(self):
        # @TODO: At this moment this path is ok, but it must be ''
        # Because if you just start the program and save, it will save 
        # a null DB on this path.
        self.__path = '../examples/CORPUS.db'
        self.__isModified = False    
    
    def addDB(self,sect=['Not Classified'],subsect=['Not Classified'],funct=['Not Classified'],phrase=['NULL'],ref=['NULL']):
        
        cursor = self.__db.cursor()
        
        whatadd = [(a,b,c,d,e) for a in sect for b in subsect for c in funct for d in phrase for e in ref]

        cursor.executemany('''INSERT INTO corpus(sec,subsec,func,phrase,ref) VALUES(?,?,?,?,?)''',whatadd)
                
        self.isModified  = True
    
    
    def listCategories(self,section=[],subsection=[],function=[]):
        
        cursor = self.__db.cursor()
        
        secsubsecfunc = []
        subsecfunc = []
        functions = []
        
        if section == [] and subsection == [] and function == []:
           cursor.execute('''SELECT DISTINCT sec, subsec, func FROM corpus''')
           secsubsecfunc = cursor.fetchall()
                
        if section != [] and subsection == [] and function == []:
           cursor.execute('SELECT DISTINCT sec, subsec, func FROM corpus WHERE sec in ({0})'.format(','.join('?' for _ in section)), section)
           subsecfunc = cursor.fetchall()
              
        if section != [] and subsection != [] and function == []:
           secsubsecTuple = [(a,b) for a in section for b in subsection]
           for i in range(len(secsubsecTuple)):
              cursor.execute('''SELECT DISTINCT sec, subsec, func FROM corpus WHERE sec=? AND subsec=?''',secsubsecTuple[i])
              functions.extend(cursor.fetchall())
        
        #sectionsFinal = []
        #subsectionsFinal = []
        #functionsFinal = []
        
        #for i in sections:
        #   sectionsFinal.append(i[0])
        
        #for i in subsections:
        #   subsectionsFinal.append(i[0])
           
        #for j in functions:
        #   for i in range(len(j)):
        #      functionsFinal.append(j[i][0])
 
        #sectionsFinal = list(set(sectionsFinal))
        #subsectionsFinal = list(set(subsectionsFinal))
        #functionsFinal = list(set(functionsFinal))

        #return [sectionsFinal,subsectionsFinal,functionsFinal]
        
        final = []
        final.extend(secsubsecfunc)
        final.extend(subsecfunc)
        final.extend(functions)
        
        #@TODO: The number of tuple must BE the SAME!
        return final


    def listSentences(self,section=[],subsection=[],function=[]):

        cursor = self.__db.cursor()
        
        phrases = []

        if section == [] and subsection == [] and function == []:
           cursor.execute('''SELECT DISTINCT sec, subsec, func, phrase, ref FROM corpus''')
           phrases.extend(cursor.fetchall())
        
        if section != [] and subsection == [] and function == []:
           cursor.execute('SELECT DISTINCT sec, subsec, func, phrase, ref FROM corpus WHERE sec in ({0})'.format(','.join('?' for _ in section)), section)
           phrases.extend(cursor.fetchall())
        
        if section != [] and subsection != [] and function == []:
           secsubsecTuple = [(a,b) for a in section for b in subsection]
           for i in range(len(secsubsecTuple)):
              cursor.execute('''SELECT DISTINCT sec, subsec, func, phrase, ref FROM corpus WHERE sec=? AND subsec=?''',secsubsecTuple[i])
              phrases.extend(cursor.fetchall())
        
        if section != [] and subsection != [] and function != []:
           secsubsecfuncTuple = [(a,b,c) for a in section for b in subsection for c in function]
           for i in range(len(secsubsecfuncTuple)):
              cursor.execute('''SELECT DISTINCT sec, subsec, func, phrase, ref FROM corpus WHERE sec=? AND subsec=? AND func=?''',secsubsecfuncTuple[i])
              phrases.extend(cursor.fetchall())
                
        return phrases
        
    def listAll(self):
        '''
        return a list o tuples with all info
        '''    
        cursor = self.__db.cursor()
        
        allInfo = []

        cursor.execute('SELECT DISCTINC sec, subsec, func, phrase, ref from corpus')
        allInfo.append(cursor.fetchall())

        return allInfo
        
        
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
                          SET func=? WHERE func=?''',function[0]) 

        if section == [('NULL','NULL')] and subsection == [('NULL','NULL')] and function == [('NULL','NULL')] and phrase != [('NULL','NULL')] and ref == [('NULL','NULL')]:
           cursor.execute('''UPDATE corpus 
                          SET phrase=? WHERE phrase=?''',phrase[0]) 
        
        if section == [('NULL','NULL')] and subsection == [('NULL','NULL')] and function == [('NULL','NULL')] and phrase == [('NULL','NULL')] and ref != [('NULL','NULL')]:
           cursor.execute('''UPDATE corpus 
                          SET ref=? WHERE ref=?''',ref[0]) 
        
        self.isModified  = True  
        
    def remove(self,sect=[],subsect=[],funct=[],phrase=[]):

        cursor = self.__db.cursor()
        
        if sect != [] and subsect == [] and funct == [] and phrase == []:
           #whatrm = [(a,) for a in sect]
           whatup = [('Not Classified',a) for a in sect]
           #cursor.executemany('DELETE FROM corpus WHERE sec=?',whatrm)
           self.update(section=whatup)
        
        if sect == [] and subsect != [] and funct == [] and phrase == []:
           #whatrm = [(a,) for a in subsect]
           whatup = [('Not Classified',a) for a in subsect]
           #cursor.executemany('DELETE FROM corpus WHERE subsec=?',whatrm)
           self.update(subsection=whatup)
           
        if sect == [] and subsect == [] and funct != [] and phrase == []:
           #whatrm = [(a,) for a in funct]
           whatup = [('Not Classified',a) for a in funct]
           #cursor.executemany('DELETE FROM corpus WHERE subsec=?',whatrm)
           self.update(function=whatup)
           
        if sect == [] and subsect == [] and funct == [] and phrase != []:
           #whatrm = [(a,) for a in phrase]
           whatup = [('NULL',a) for a in phrase]
           #cursor.executemany('DELETE FROM corpus WHERE subsec=?',whatrm)
           self.update(phrase=whatup)

        self.isModified  = True


    def bulk_add(self, path):
            
        cursor = self.__db.cursor()
        
        tree = ET.parse(path)      
        root = tree.getroot()
        
        info = [(w.find('SECTION').text, w.find('SUBSECTION').text, w.find('FUNCTION').text, w.find('PHRASE').text, w.find('REF').text) for w in root.findall('INFOPIECE')]
        
        cursor.executemany('INSERT INTO corpus(sec,subsec,func,phrase,ref) VALUES(?,?,?,?,?)',info)
        
        self.isModified  = True
      
    
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
    def db(self):
        self.__db

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
        
        try:
           self.__db.commit()
        except Exception:
           raise
        else:
           self.isModified = False
        
    def read_(self,  path):
        """
        Reads file.
        """
        
        try:
            self.__db = sqlite3.connect(path)
            cur = self.__db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS
                        corpus(id INTEGER PRIMARY KEY, sec TEXT, subsec TEXT,
                        func TEXT, phrase TEXT, ref TEXT)''')
            self.__db.commit()
        except Exception:
            raise
        else:
            self.path = path
            self.isModified = False
        
      
    def close_(self):
        """
        Clear all fields.
        """
        
        try:
           self.__db.close()
        except Exception:
           raise
        else:
           self.__path = ''
           self.__isModified = False        
        
    def import_(self,  path=''):
        """
        Import file as XML, JSON, DB.
        """
        try:
           extension = path.split('.')[1]
           if extension == 'xml' or 'XML':
              self.bulk_add(path)
        except Exception:
           raise
        else:
           self.isModified = True
        
    def export_(self,  path=''):
        """
        Export file as XML, JSON, DB.
        """

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
        
        try:
            self.__db = sqlite3.connect(path)
            cur = self.__db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS
                        corpus(id INTEGER PRIMARY KEY, sec TEXT, subsec TEXT,
                        func TEXT, phrase TEXT, ref TEXT)''')
            self.__db.commit()
        except Exception:
            raise
        else:
            self.path = path
            self.isModified = False
        
    def clear_(self):
        """
        Clear all fields.
        """
        self.__path = ''
        self.__isModified = False
        #self.__dict = {'Not Classified':{'Not Classified':{'Not Classified':('Sentence','Reference')}}}
        self.__db.commit()
        self.__db.close()
        
    def import_(self,  path=''):
        """
        Import file as XML, JSON, DB.
        """
        extension = path.split('.')[1]
        
        if extension == 'xml' or 'XML':
           self.bulk_add(path)
        
        self.isModified = True
        
    def export_(self,  path=''):
        """
        Export file as XML, JSON, DB.
        """
        print path
        with codecs.open(path, 'wb',  'utf-8') as project_file:
            json.dump(self.__dict, project_file,  indent=4,  sort_keys=True)
        self.isModified = False

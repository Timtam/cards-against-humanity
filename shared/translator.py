from .path import getScriptDirectory

import lxml.etree as ET
import os
import os.path

class Translator(object):

  def __init__(self, node):
    self.node = node
    self.init()

  def getAvailableLanguages(self):
    return [self.getDefaultLanguage()]+[os.path.splitext(lang)[0] for lang in os.listdir(self.getLanguageFolder())]

  @staticmethod
  def getDefaultLanguage():
    return 'English'

  @staticmethod
  def getLanguageFolder():
    return os.path.join(getScriptDirectory(), 'languages')

  def setLanguage(self, language):
    self.close()
    if language != self.getDefaultLanguage() and language in self.getAvailableLanguages():
      self.language = language
      xml = self.openXml(os.path.join(self.getLanguageFolder(), language+'.xml'))
      self.xml = xml.getroot().xpath(self.node)[0]
      if not os.path.exists(os.path.join(getScriptDirectory(), 'untranslated')):
        os.makedirs(os.path.join(getScriptDirectory(), 'untranslated'))
      self.untranslated_xml = self.openXml(os.path.join(getScriptDirectory(), 'untranslated', language+'.xml'))

  def getLanguage(self):
    return self.language

  def translate(self, string):

    if self.xml is not None:
      translations = self.xml.xpath('string/origin[text() = "'+string+'"]/../translation')
      if len(translations)>0:
        return translations[0].text
      else:
        # untranslated strings will be stored inside a xml document
        node = self.untranslated_xml.getroot().xpath(self.node)[0]
        if len(node.xpath('string/origin[text() = "'+string+'"]/../translation'))==0:
          element = ET.SubElement(node, "string")
          origin = ET.SubElement(element, "origin")
          origin.text = string
          translation = ET.SubElement(element, "translation")
          translation.text = string

    return string

  def close(self):
    if self.untranslated_xml is not None and len(self.untranslated_xml.getroot().xpath(self.node)[0])>0:
      # we got some untranslated strings
      # we will store them inside a file
      self.untranslated_xml.write(os.path.join(getScriptDirectory(), 'untranslated', self.language+'.xml'), pretty_print = True, encoding = 'utf-8', xml_declaration=True)
    self.init()

  def init(self):
    self.language = self.getDefaultLanguage()
    self.untranslated_xml = None
    self.xml = None

  def openXml(self, path):
    if not os.path.exists(path):
      element = ET.Element('translations')
      xml = ET.ElementTree(element)
      ET.SubElement(element, self.node)
    else:
      xml = ET.parse(path)
      element = xml.getroot().xpath(self.node)
      if len(element) == 0:
        element = ET.SubElement(xml.getroot(), self.node)

    return xml

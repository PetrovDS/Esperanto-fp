import re
import numpy as np

class Esperanto():

    ALPHABET = "abcĉdefgĝhĥijĵklmnoprsŝtuŭvz"
    PUNCTUATION = "-–\"',.:;?!()"

    ENDINGS = ["o", "a", "e", "i", "as", "is", "os", "us", "u"]
    ENDINGS_DESC = ["существительное", "прилагательное", "наречие", "инфинитив", "глагол настоящего времени",
                    "глагол прошедшего времени", "глагол будущего времени", "глагол в условно-сослагательном наклонении", "глагол повелительного наклонения"]

    PREFIXES = ["bo", "dis", "ek", "eks", "fi", "ge", "mal", "mis", "pra", "re"][::-1]
    PREFIXES_DESC = ["свойство, родство по браку", "разъединение", "начало или мгновенность действия", "бывший, экс-", "противный, мерзкий",
                     "обоих полов", "антоним", "ошибочность, неверность, оплошность", "далёкая степень родства; первобытность", "обратное или повторное действие"][::-1]

    SUFFIXES = ["ac", "aĉ", "ad", "aĵ", "al", "an", "ant", "ar", "at", "ĉj", "ebl", "ec", "ed", "eg", "ej", "em", "end", "er", "esk", "estr", "et", "i", "iĉ", "id", "ig",
                "iĝ", "ik", "il", "in", "ind", "ing", "int", "ism", "ist", "it", "iv", "iz", "nj", "obl", "ol", "on", "ont", "op", "ot", "oz", "uj", "uk", "ul", "um", "unt", "ut"][::-1]
    SUFFIXES_DESC = ["употребляется в ботанической терминологии для наименования семейств", "низкое качество, никчёмный, уничижительный", "длительность, продолжительность действия", 
                "конкретное проявление признака", "в ботанической номенклатуре — порядок; в химической — альдегид; в анатомической — кость", "член, последователь, участник, житель", 
                "действительное причастие настоящего времени", "совокупность", "пассивное причастие настоящего времени; в химической номенклатуре — соль кислоты с большим содержанием кислорода", 
                "мужская ласкательная форма; усекает корень", "пассивная возможность", "свойство, качество", "в зоологической номенклатуре — семейство", 
                "увеличение, усиление; иногда уничижительная коннотация при обозначении людей", "место, помещение (не используется для топонимов)", "склонность к чему-либо, тенденции", 
                "«который должен быть»", "частица чего-либо", "«в стиле, по манере, вроде»", "главная персона, начальник", "уменьшение, ослабление; иногда ласковая коннотация при обозначении людей", 
                "страна; группа стран; наука; политический режим (нельзя использовать в качестве корня «io», так как это означает «что-то»)", "мужской пол", "потомок, детёныш", 
                "делать каким-либо, кем-либо, чем-либо", "делаться каким-либо, кем-либо, чем-либо", 
                "вид искусства, наука, техника, названия которых образованны от названия деятеля/предмета; окисла или соли, в которых металл проявляет большую валентность", 
                "орудие, инструмент, средство", "женский пол", "достойный чего-либо", "то, куда вставляется", "действительное причастие прошедшего времени", 
                "общественное движение, учение, особенности языка, пристрастие к чему-либо", "человек определённой профессии, убеждений, сторонник общественного движения, учения", 
                "страдательное причастие прошедшего времени; в химической номенклатуре — соль кислоты с меньшим содержанием кислорода; в медицинской — заболевание воспалительного характера", 
                "способный, могущий", "снабжать, покрывать, добавлять", "женский ласкательный суффикс; усекает корень", "множественные числительные", 
                "в химической номенклатуре — спирт, название которого образовано от названий соответствующих углеводородов", "дробные числительные", "действительное причастие будущего времени",
                "собирательные числительные", "страдательное причастие будущего времени", "обильный, насыщенный, полный, имеющий, богатый", "то, в чём хранится; дерево, на котором растёт; страна", 
                "кастрированное животное", "лицо, обладающее данным качеством", "без определённого значения, применяется когда другие суффиксы не подходят", "действительное условное причастие", 
                "страдательное условное причастие"][::-1]

    PREPOSITIONS = ["al", "anstataŭ", "antaŭ", "apud", "ĉe", "ĉirkaŭ", "da", "de", "dum", "ekster", "el", "en", "ĝis", "inter", "je", "kontraŭ",
                    "krom", "kun", "laŭ", "malgraŭ", "per", "po", "por", "post", "preter", "pri", "pro", "sen", "sub", "super", "sur", "tra", "trans"]
    
    PRONOUNS = ["mi", "ni", "vi", "li", "ŝi", "ĝi", "ili", "oni", "si"]

    NUMERAL = ["nul", "unu", "du", "tri", "kvar", "kvin",
               "ses", "sep", "ok", "naŭ", "dek", "cent", "mil", "miliono", "miliardo", "biliono", "triliono"]

    CONJUNCTION = ["kaj", "aŭ", "sed", "plus", "minus", "nek"]
    S_CONJUNCTION = ["ke", "ĉu", "se", "ĉar", "dum",
                   "ĝis", "kvankam", "kvazaŭ", "ol", "apenaŭ"]

    PARTICLE = ["pli", "plej", "ne", "ĉi", "for", "ankoraŭ", "baldaŭ", "hodiaŭ", "hieraŭ", "morgaŭ", "jam", "ĵus", "nun", "plu", "tuj", "ajn",
         "almenaŭ", "ankaŭ", "apenaŭ", "des", "do", "eĉ", "ja", "jen", "jes", "ju", "kvazaŭ", "mem", "nur", "preskaŭ", "tamen", "tre", "tro"]

    TABLE_W_PREFIX = ["ki", "ti", "i", "ĉi", "neni"]
    TABLE_W_PREFIX_DESC = ["вопросительное слово, относительное слово, восклицательное слово",
                           "слово-указатель", "неопределенное слово", "всё-слово", "отрицательное слово"]

    TABLE_W_ENDING = ["u", "o", "a", "es", "e", "am", "al", "el", "om"]
    TABLE_W_ENDING_DESC = ["индивид, отдельная вещь, отдельный предмет", "вещь", "свойство, разновидность",
                           "владелец (смысловой объект или субъект)", "место", "время, случай (событие, условие)", "причина", "способ, степень", "количество"]


    def __init__(self, text=""):
        self.text = self._clean(text)

        if self.is_sentence():
            reg = re.compile(f"[^{self.ALPHABET}0-9]", re.IGNORECASE)
            self.words_list = [Esperanto(reg.sub("", word)) for word in self.text.split()]
        else:
            self.word_list = None

    def _clean(self, text):
        #reg = re.compile(f"[^{self.PUNCTUATION}{self.ALPHABET}0-9 ]", re.IGNORECASE)
        reg = re.compile(f"[^{self.ALPHABET}0-9 ]")
        return reg.sub("", text.lower()).replace(" +", "").strip()

    def is_word(self):
        return self.text.find(" ") == -1 and not self.is_empty()

    def is_sentence(self):
        return self.text.find(" ") != -1

    def is_number(self):
        reg = re.compile(f"^[{self.PUNCTUATION}0-9 ]+$")
        return re.match(reg, self.text) is not None

    def is_empty(self):
        return self.text == ""

    def describe(self, mode="description"):
        assert mode in ["description", "vector", "both"], 'mode может иметь только значения "description", "vector" или "both"'
        if not self.is_word():
            if mode == "description":
                return []
            elif mode == "vector":
                return np.array([0 for i in range(94)] + [1], dtype=np.float32)
            elif mode == "both":
                return [], np.array([0 for i in range(94)] + [1], dtype=np.float32)
        else:
            vect = []
            prop = []
            #reg = re.compile(f"[^{self.ALPHABET}]")
            #word = reg.sub("", self.text.lower())
            word = self.text
            spec_flag = False

            # определяем предлоги
            if word in self.PREPOSITIONS:
                prop.append("предлог")
                vect.append(1)
                spec_flag = True
            else:
                vect.append(0)

            # определяем табличные слова
            if spec_flag:
                vect.extend([0 for i in range(15)])
            else:
                tmp_prefix = ""
                tmp_ending = ""
                for pref in self.TABLE_W_PREFIX:
                    if word.startswith(pref):
                        tmp_prefix = pref
                        break
                for ending in self.TABLE_W_ENDING:
                    if word.endswith(ending):
                        tmp_ending = ending
                        break
                if tmp_prefix and tmp_ending and word == tmp_prefix + tmp_ending:
                    prop.append("табличное слово")
                    vect.append(1)
                    prop.append(self.TABLE_W_PREFIX_DESC[self.TABLE_W_PREFIX.index(tmp_prefix)])
                    prop.append(self.TABLE_W_ENDING_DESC[self.TABLE_W_ENDING.index(tmp_ending)])
                    tmp_vect = [0 for i in range(len(self.TABLE_W_PREFIX))]
                    tmp_vect[self.TABLE_W_PREFIX.index(tmp_prefix)] = 1
                    vect.extend(tmp_vect)
                    tmp_vect = [0 for i in range(len(self.TABLE_W_ENDING))]
                    tmp_vect[self.TABLE_W_ENDING.index(tmp_ending)] = 1
                    vect.extend(tmp_vect)
                    spec_flag = True
                else:
                    vect.extend([0 for i in range(15)])

            # определяем союзы
            if spec_flag:
                vect.append(0)
            elif word in self.CONJUNCTION:
                prop.append("союз")
                vect.append(1)
                spec_flag = True
            else:
                vect.append(0)

            # определяем подчинительные союзы
            if spec_flag:
                vect.append(0)
            elif word in self.S_CONJUNCTION:
                prop.append("подченительный союз")
                vect.append(1)
                spec_flag = True
            else:
                vect.append(0)

            # определяем подчинительные союзы
            if spec_flag:
                vect.append(0)
            elif word in self.PARTICLE:
                prop.append("частица")
                vect.append(1)
                spec_flag = True
            else:
                vect.append(0)
            
            # определяем числительные
            if spec_flag:
                vect.append(0)
            elif word in self.NUMERAL or len(word) > 4 and (word[-3:] == "dek" or word[-4:] == "cent"):
                prop.append("числительное")
                vect.append(1)
                spec_flag = True
            else:
                vect.append(0)
            
            # форма другихчастей речи
            if spec_flag or word in ["j", "n", "jn"]:
                vect.extend([0, 0])
            else:
                if word[-1] == "n":
                    prop.append("винительный падеж")
                    vect.append(1)
                    word = word[:-1]
                else:
                    vect.append(0)
                if word[-1] == "j":
                    prop.append("множественное число")
                    vect.append(1)
                    word = word[:-1]
                else:
                    prop.append("единственное число")
                    vect.append(0)

            # определяем местоимения
            if spec_flag:
                vect.extend([0, 0])
            elif word in self.PRONOUNS:
                prop.append("личное местоимение")
                vect.extend([1, 0])
                spec_flag = True
            elif word[-1:] in self.PRONOUNS and word[-1] == "a":
                prop.append("притяжательное местоимение")
                vect.extend([0, 1])
                spec_flag = True
            else:
                vect.extend([0, 0])

            # другие части речи
            if spec_flag:
                vect.extend([0 for i in self.ENDINGS])
                vect.extend([0 for i in self.PREFIXES])
                vect.extend([0 for i in self.SUFFIXES])
                is_incorrect = 0
            else:
                is_incorrect = 1
                for i, ending in enumerate(self.ENDINGS):
                    if self.text.endswith(ending):
                        is_incorrect = 0
                        vect.append(1)
                        #prop.append([ending, self.ENDINGS_DESC[i]])
                        prop.append(self.ENDINGS_DESC[i])
                    else:
                        vect.append(0)

                for i, prefix in enumerate(self.PREFIXES):
                    if self.text.startswith(prefix):
                        vect.append(1)
                        #prop.append([prefix, self.PREFIXES_DESC[i]])
                        prop.append(self.PREFIXES_DESC[i])
                    else:
                        vect.append(0)
                for i, suffix in enumerate(self.SUFFIXES):
                    if self.text.find(suffix) > 0:
                        vect.append(1)
                        #prop.append([suffix, self.SUFFIXES_DESC[i]])
                        prop.append(self.SUFFIXES_DESC[i])
                    else:
                        vect.append(0)
            vect.append(is_incorrect)
            vect = np.array(vect, dtype=np.float32)
            if mode == "description":
                return prop
            elif mode == "vector":
                return vect
            elif mode == "both":
                return prop, vect

    @property
    def type(self):
        if self.is_word():
            return "word"
        elif self.is_sentence():
            return "sentence"
        elif self.is_number():
            return "number"
        elif self.is_empty():
            return "empty"
        else:
            return "special"
    
    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Esperanto('{self.text}', type='{self.type}')"

if __name__ == '__main__':
    t = "Tiu ĉi rakonto estas pri la vivo en la jaro 829, en vikinga vilaĝo (la nuna Svedujo). ARNE estas knabeto. Li vivas apud la maro kaj la vilaĝanoj (ĉar ili sendube preferas pacon) temas ĉiutage pri piratoj."
    t = Esperanto(t).words_list
    for i in t:
        if len(i.describe()) > 1:
            print(i, i.describe())

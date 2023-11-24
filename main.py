import re
import sys
from const import *




class CPE_2_3:
    """
    Class for validating and parsing Common Platform Enumeration (CPE) 2.3 strings.

    Methods:
    - component_validator(self, value: str) -> str:
        Validates a Common Platform Enumeration (CPE) component value.

    - language_validator(self, value: str) -> str:
        Validates a language value used in a Common Platform Enumeration (CPE).

    - parse_cpe(self, cpe_str: str) -> dict:
        Parses a Common Platform Enumeration (CPE) string and returns a dictionary containing the extracted components.
    """

    #  component validator variables
    _logical = "(\{0}|{1})".format(VALUE_ANY, VALUE_NA)
    _quest = "\{0}".format(WILDCARD_ONE)
    _asterisk = "\{0}".format(WILDCARD_MULTI)
    _special = "{0}|{1}".format(_quest, _asterisk)
    _spec_chrs = "{0}+|{1}".format(_quest, _asterisk)
    _quoted = r"\\(\\" + "|{0}|{1})".format(_special, PUNC)
    _avstring = "{0}|{1}".format(UNRESERVED, _quoted)
    _value_string_pattern = "^(({0}+|{1}*({2})+|{3}({4})+)({5})?|{6})$".format(
        _quest, _quest, _avstring, _asterisk, _avstring, _spec_chrs, _logical)
    _part_value_rxc = re.compile(_value_string_pattern)

    #  language validator variables
    _language_pattern = re.compile(r"^[a-z]{2,3}-(?:[A-Z]{2,3}|\d{3})$")

    #  CPE_2_3 validator variables
    _COMP_RE = "(?P<{0}>.*?)(?<!\\\\)"
    _logical = "\\{0}|\\{1}".format(
        VALUE_ANY, VALUE_NA)
    _typesys = "(?P<{0}>(h|o|a|{1}))".format(
        ATT_PART, _logical)
    _vendor = _COMP_RE.format(ATT_VENDOR)
    _product = _COMP_RE.format(ATT_PRODUCT)
    _version = _COMP_RE.format(ATT_VERSION)
    _update = _COMP_RE.format(ATT_UPDATE)
    _edition = _COMP_RE.format(ATT_EDITION)
    _language = _COMP_RE.format(ATT_LANGUAGE)
    _sw_edition = _COMP_RE.format(ATT_SW_EDITION)
    _target_sw = _COMP_RE.format(ATT_TARGET_SW)
    _target_hw = _COMP_RE.format(ATT_TARGET_HW)
    _other = _COMP_RE.format(ATT_OTHER)


    _parts_pattern = "^cpe:2.3:{0}\:{1}\:{2}\:{3}\:{4}\:{5}\:{6}\:{7}\:{8}\:{9}\:{10}$".format(
        _typesys, _vendor, _product, _version, _update, _edition,
        _language, _sw_edition, _target_sw, _target_hw, _other)

    _parts_rxc = re.compile(_parts_pattern, re.IGNORECASE)


    def component_validator(self, value: str) -> str:
        """
        Validates a Common Platform Enumeration (CPE) component value.

        Parameters:
        - value (str): The CPE component value to be validated.

        Returns:
        - str: The validated CPE component value.

        Raises:
        - ValueError: If the input CPE component value is not well-formed.

        """
        parts_match =self._part_value_rxc.match(value) 

        if (parts_match is None):
            msg = "Bad-formed CPE"
            raise ValueError(msg)
        return parts_match.group()


    def language_validator(self, value: str) -> str:
        """
        Validates a language value used in a Common Platform Enumeration (CPE).

        Parameters:
        - value (str): The language value to be validated.

        Returns:
        - str: The validated language value.

        Raises:
        - ValueError: If the input language value is not well-formed.

        """
        if not self._language_pattern.match(value):
            errmsg = "Bad-formed CPE"
            raise ValueError(errmsg)
        return value

    def parse_cpe(self,cpe_str:str) -> dict:
        """
        Parses a Common Platform Enumeration (CPE) string and returns a dictionary
        containing the extracted components.

        Parameters:
        - cpe_str (str): The CPE string to be parsed.

        Returns:
        - dict: A dictionary containing the parsed components of the CPE.

        Raises:
        - ValueError: If the input CPE string is not well-formed.
        """

        if (cpe_str.find(" ") != -1):
            msg = "Bad-formed CPE"
            raise ValueError(msg)

        parts_match = self._parts_rxc.match(cpe_str)

        if (parts_match is None):
            msg = "Bad-formed CPE"
            raise ValueError(msg)

        parts_match_dict = parts_match.groupdict()

        if (parts_match is None):
            msg = "Bad-formed CPE"
            raise ValueError(msg)

        components = dict()
        parts_match_dict = parts_match.groupdict()

        for ck in CPE_COMP_KEYS_EXTENDED:
            if ck in parts_match_dict:
                value = parts_match.group(ck)

                if (value == VALUE_ANY):
                    comp = "ANY"
                elif (value == VALUE_NA):
                    comp = "NA"
                elif (ck == ATT_LANGUAGE) and (value != VALUE_ANY):
                    comp = self.language_validator(value)
                else:
                    try:
                        comp = self.component_validator(value)
                    except ValueError:
                        errmsg = "Bad-formed CPE"
                        raise ValueError(errmsg)
            else:
                errmsg = "Bad-formed CPE"
                raise ValueError(ck)

            components[ck] = comp
        return components

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python twoj_skrypt.py <ciąg_CPE_2.3>")
        sys.exit(1)

    cpe_str = sys.argv[1]
    result_dict = CPE_2_3().parse_cpe(cpe_str)
    print(result_dict)

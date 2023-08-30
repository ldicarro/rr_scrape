class TextUtil:
    """
    convert newlines to <br> tags

    Parameters
    ----------
    txt: string

    Returns
    -------
    string: modified txt
    """
    def formatRawText(self,txt):
        return txt.replace('\n','<br>')
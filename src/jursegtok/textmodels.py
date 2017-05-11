
class TextCollection(object):
    """
    An Iterator or graph for text
    """
    pass


class Text(object):
    """
    a single text segment without constraints
    """
    pass


class Paragraph(Text):
    """
    a paragraph segment
    """
    pass


class Sentence(Text):
    """
    defines a sentence.
    """
    def __init__(self):
        pass
    



class Statement(Text):
    pass


class Reference(Text):
    pass


class Norm(Reference):
    pass


class Publication(Reference):
    pass

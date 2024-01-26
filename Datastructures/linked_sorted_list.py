"""
-------------------------------------------------------
Linked Sorted List; 
-------------------------------------------------------
Author:  JD
ID:      #
Email:   jsingh@live.com
__updated__ = "2023-05-27"
-------------------------------------------------------
"""


class _SL_Node:
    def __init__(self, value, date, _next):
        """
        -------------------------------------------------------
        Initializes a sorted list node. Sorts values acc. to date
        Use: node = _SL_Node(value, date,_next)
        -------------------------------------------------------
        Parameters:
            value - value value for node (?)
            date  - date(datetime.obj)
            next_ - another sorted list node (_SL_Node)
        Returns:
            Initializes a list node that contains a copy of value
            and a link to the next node in the list.
        -------------------------------------------------------
        """
        self._value = value
        self._next = _next
        self._date = date



class SortedList:
    def __init__(self):
        """
        -------------------------------------------------------
        Initializes an empty Sorted_List.
        Use: sl = Sorted_List()
        -------------------------------------------------------
        Returns:
            a Sorted_List object (Sorted_List)
        -------------------------------------------------------
        """
        self._front = None
        self._rear = None
        self._count = 0

    def __len__(self):
        """
        -------------------------------------------------------
        Returns the size of the list.
        Use: n = len(l)
        -------------------------------------------------------
        Returns:
            Returns the number of values in the list.
        -------------------------------------------------------
        """
        return self._count

    def append(self, value, date):
        """
        -------------------------------------------------------
        Inserts value at the proper place in the sorted list.
        Use: sl.append(value)
        -------------------------------------------------------
        Parameters:
            value - a data element (?)
        Returns:
            None
        -------------------------------------------------------
        """
        node = _SL_Node(value, date, None)
        if self._count == 0:
            self._front = node
            self._rear = node

        else:
            curr = self._front
            prev = None
            while curr is not None and curr._date <= date:
                prev = curr
                curr = curr._next

            if curr == self._front:
                node._next = self._front
                self._front = node
            elif curr is None:
                self._rear._next = node
                self._rear = node
            else:
                prev._next = node
                node._next = curr
        self._count += 1

    def __iter__(self):
        curr = self._front
        while curr is not None:
            yield curr._value
            curr = curr._next

    def last(self):
        return self._rear

"""
OOP solution for day 13.
"""
from __future__ import annotations

import collections.abc
import math
from typing import Any


def list_to_packet(value: Any) -> Packet | int | None:
    if value is None:
        return value

    return Packet(value) if isinstance(value, list) else value


class Packet(collections.abc.MutableSequence):
    """
    A packet, which is a list of integers or other packets.

    This inheritance implementation is based on the following:
    - https://github.com/python/cpython/blob/208a7e957b812ad3b3733791845447677a704f3e/Lib/collections/__init__.py#L1174
    """

    def __init__(self, items: Packet | list = None):
        """
        Create a Packet, which is a list of integers or other packets.
        """
        self.data = []
        if items is not None:
            if isinstance(items, Packet):
                self.data[:] = items.data[:]
            elif isinstance(items, int):
                self.data[:] = [items]
            else:
                self.data = list(items)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f"Packet(items={self.data})"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i: int):
        return self.__class__(self.data[i]) if isinstance(i, slice) else self.data[i]

    def __setitem__(self, i: int, item: Any):
        self.data[i] = item

    def __delitem__(self, i: int):
        del self.data[i]

    def __eq__(self, other: Packet | list):
        other = other if isinstance(other, Packet) else Packet(other)
        return self.data == other.data

    def __lt__(self, other: Packet | int):
        """
        Compare 2 packets element-wise.
        """
        other = other if isinstance(other, Packet) else Packet(other)

        # sourcery skip: merge-duplicate-blocks, remove-redundant-if
        for i in range(max(len(self), len(other))):
            left, right = list_to_packet(self.get(i)), list_to_packet(other.get(i))
            # print(f"Compare {left} vs {right}")

            if left is None and right is not None:
                # The left packet is smaller
                # print("Left side ran out of items, so inputs are in the right order")
                return True
            elif right is None:
                # The right packet is smaller
                # print("Right side ran out of items, so inputs are not in the right order")
                return False

            if type(left) != type(right):
                if isinstance(left, int):
                    # print(f"Mixed types; convert left to [{left}] and retry comparison")
                    left = Packet([left])
                elif isinstance(right, int):
                    # print(f"Mixed types; convert right to [{right}] and retry comparison")
                    right = Packet([right])

            if left < right:
                # The left packet is smaller
                # print(f"    Left side is smaller, so inputs are in the right order ({left} < {right})")
                return True
            elif left > right:
                # The right packet is smaller
                # print(f"    Right side is smaller, so inputs are not in the right order ({left} > {right})")
                return False

        return False

    def __le__(self, other: Packet):
        return self < other or self == other

    def __gt__(self, other: Packet):
        return not (self <= other)

    def __ge__(self, other: Packet):
        return self > other or self == other

    def insert(self, i: int, item: Any) -> None:
        """
        Insert an item at index i.
        """
        self.data.insert(i, item)

    def get(self, index_: int, default: Any = None) -> Any:
        """
        Get the value at the index, returning 0 if the index does not exist.
        """
        if index_ < 0 or not isinstance(index_, int):
            raise IndexError(f"Packet index {index_} is out of range")

        try:
            return self[index_]
        except IndexError:
            return default

    @classmethod
    def from_text(cls, text: str) -> Packet:
        """
        Convert the text representation into a packet.
        """
        return cls(list(eval(text)))


class PacketPair:
    """
    A pair of packets.
    """

    def __init__(self, left_packet: Packet, right_packet: Packet):
        self.left_packet = left_packet
        self.right_packet = right_packet

    def __str__(self):
        return f"<{self.left_packet}><{self.right_packet}>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield from [self.left_packet, self.right_packet]

    @classmethod
    def from_text(cls, text: str) -> PacketPair:
        """
        Parse a textual pair of packets into a PacketPair.
        """
        left, right = text.split("\n")
        return cls(Packet.from_text(left), Packet.from_text(right))


class PacketPairs:
    def __init__(self, packet_pairs: dict[int, PacketPair]):
        self.packet_pairs = packet_pairs

    @classmethod
    def from_text(cls, text: str) -> PacketPairs:
        return cls(
            {
                i + 1: PacketPair.from_text(text)
                for i, text in enumerate(text.split("\n\n"))
            }
        )

    def pairs_in_correct_order(self) -> int:
        index_sum = 0
        for pair, packet_pair in self.packet_pairs.items():
            packet_1, packet_2 = packet_pair
            if packet_1 < packet_2:
                index_sum += pair

        return index_sum


class Packets:
    def __init__(self, packets: list[Packet], divider_packets: list[Packet]):
        self.packets = packets + divider_packets
        self.divider_packets = divider_packets

    @classmethod
    def from_text(cls, packet_text: str, divider_packets: list[Packet]) -> Packets:
        return cls(
            [
                Packet.from_text(packet)
                for packet in packet_text.split("\n")
                if packet != ""
            ],
            divider_packets,
        )

    def find_distress_signal(self) -> int:
        packets = sorted(self.packets)

        return math.prod(1 + packets.index(divider) for divider in self.divider_packets)


def solution(input_: str) -> list[Any]:
    """
    Solve the day 13 problem!
    """
    packet_pairs = PacketPairs.from_text(input_.strip())
    divider_packets = [
        Packet.from_text("[[2]]"),
        Packet.from_text("[[6]]"),
    ]
    packets = Packets.from_text(input_.strip(), divider_packets)

    return [
        packet_pairs.pairs_in_correct_order(),
        packets.find_distress_signal(),
    ]

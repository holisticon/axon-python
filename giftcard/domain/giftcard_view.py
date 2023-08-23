import dataclasses
from domain.view import IView
from giftcard.payloads import *


@dataclasses.dataclass
class GiftCardSummary:
    id: str
    initialAmount: int
    remainingAmount: int
    isActive: bool = True


class GiftCardSummaryView(IView[GiftCardSummary, GiftCardEvent]):
    @property
    def initial_state(self) -> GiftCardSummary | None:
        return None

    def evolve(
        self, state: GiftCardSummary | None, event: GiftCardEvent
    ) -> GiftCardSummary:
        match event:
            case CardIssuedEvent():
                return GiftCardSummary(
                    id=event.id,
                    initialAmount=event.amount,
                    remainingAmount=event.amount,
                )
            case CardRedeemedEvent():
                if state:
                    return GiftCardSummary(
                        id=state.id,
                        initialAmount=state.initialAmount,
                        remainingAmount=state.remainingAmount - event.amount,
                    )
            case CardCanceledEvent():
                if state:
                    return GiftCardSummary(
                        id=state.id,
                        initialAmount=state.initialAmount,
                        remainingAmount=0,
                        isActive=False,
                    )
            case _:
                print(f"Nothing found for {event}")

        raise ValueError(f"Unexpected event {event}")
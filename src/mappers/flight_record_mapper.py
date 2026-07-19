from src.models.flight_record import FlightRecord


class FlightRecordMapper:

    @staticmethod
    def from_row(row) -> FlightRecord:

        return FlightRecord(
            searched_at=row[0],
            origin=row[1],
            destination=row[2],
            departure_date=row[3],
            airline=row[4],
            departure=row[5],
            arrival=row[6],
            duration=row[7],
            route=row[8],
            stops=row[9],
            price=row[10],
        )
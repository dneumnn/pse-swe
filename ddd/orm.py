from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

import model

mapper_registry = registry()

order_lines = Table("order_lines", 
                    mapper_registry.metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("order_id", String(255)),
                    Column("stock_keeping_unit", String(255)),
                    Column("quantity", Integer, nullable=False),
                    )

batches = Table("batches",
                mapper_registry.metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("reference", String(255)),
                Column("stock_keeping_unit", String(255)),
                Column("_purchased_quantity", Integer, nullable=False),
                Column("eta", Date, nullable=True),
                )

allocations = Table("allocations",
                    mapper_registry.metadata,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("orderline_id", ForeignKey("order_lines.id")),
                    Column("batch_id", ForeignKey("batches.id")),
                    )

#mapper_registry.map_imperatively(model.OrderLine, order_lines)

lines_mapper = mapper_registry.map_imperatively(
    model.OrderLine,
    order_lines
    )

mapper_registry.map_imperatively(
    model.Batch, 
    batches,
    properties={"_allocations": relationship(lines_mapper,
                                            secondary=allocations, 
                                            collection_class=set
                                            )
            },
    )


def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(
        model.OrderLine,
        order_lines
    )

    mapper_registry.map_imperatively(
        model.Batch, 
        batches,
        properties={"_allocations": relationship(lines_mapper,
                                                secondary=allocations, 
                                                collection_class=set
                                                )
                    },
    )
    
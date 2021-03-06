from pydantic import BaseModel


class DnsRequestCreateForm(BaseModel):
    name: str
    source_address: str
    source_port: int
    type: str
    protocol: str
    dns_server_name: str

from asyncua import Server, ua


class OPCUAServer:
    def __init__(self, endpoint="opc.tcp://0.0.0.0:4840", namespace="lab-usine"):
        self.endpoint = endpoint
        self.namespace = namespace
        self.server = None
        self.idx = None
        self.objects = None
        self._nodes: dict[str, object] = {}
        self._variables: dict[str, object] = {}
    
    @property
    def equipment_nodes(self) -> dict:
        return self._nodes

    @property
    def variables(self) -> dict:
        return self._variables

    async def _setup(self):
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint(self.endpoint)
        self.server.set_server_name("LabUsine OPC UA Server")
        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        self.idx = await self.server.register_namespace(self.namespace)
        self.objects = self.server.get_objects_node()

    async def create_equipment_node(self, name: str, parent: str | None = None) -> None:
        parent_node = self._nodes.get(parent) if parent else self.objects
        if parent_node is None:
            raise ValueError(f"Parent '{parent}' not found.")
        node = await parent_node.add_object(self.idx, name)
        self._nodes[name] = node

    async def add_variable(self, equipment_name: str, variable_name: str, initial_value, writable=False):
        node = self._nodes.get(equipment_name)
        if node is None:
            raise ValueError(f"Equipment '{equipment_name}' not found.")
        var = await node.add_variable(self.idx, variable_name, initial_value)
        if writable:
            await var.set_writable()
        self._variables[f"{equipment_name}.{variable_name}"] = var
        return var

    async def set_value(self, equipment_name: str, variable_name: str, value):
        key = f"{equipment_name}.{variable_name}"
        var = self._variables.get(key)
        if var is None:
            raise ValueError(f"Variable '{key}' not found.")
        await var.write_value(value)

    async def get_value(self, equipment_name: str, variable_name: str):
        key = f"{equipment_name}.{variable_name}"
        var = self._variables.get(key)
        if var is None:
            raise ValueError(f"Variable '{key}' not found.")
        return await var.read_value()

    async def start(self):
        await self._setup()
        await self.server.start()
        print(f"OPC UA Server started at {self.endpoint}")

    async def stop(self):
        await self.server.stop()
        print("OPC UA Server stopped.")

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *args):
        await self.stop()
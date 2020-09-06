local component = require("component")  
local net = component.internet

-- Remote proxy
local remote = net.connect("ctf.bricked.tech", 1337)  
-- Local minecraft server
local local_serv = net.connect("0.0.0.0", 31337)  

local size = 4096

if (remote and local_serv) then
	print("Connected to both servers")
	local data
	while(remote and local_serv) do
		-- [remote] --> [alles]
		data = remote.read(size)
		if data then
--			print(data)
			local_serv.write(data)
		end
		-- [alles] --> [remote]
		data = local_serv.read(size)
		if data then
--			print(data)
			remote.write(data)
		end
	end
end

remote:close() 
local_serv:close()


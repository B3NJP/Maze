
function love.load()
	toggle = false
	start = {}
	connections = {}
	finish = {}
	height = 50
	width = 50
	randomSeed = os.time()
	math.randomseed(randomSeed)
	-- generating maze
	grid = {}
	for i=1, height do
		grid[i] = {}
		for o=1, width do
			grid[i][o] = 0
		end
	end
	start, finish, connections = mazeGenerate(height, width)
	connectionPath = {}
end

function love.update(dt)
	-- body
		
	if love.keyboard.isDown('o') and go then
		connectionPath = mazeSolve({1, 1}, {width, height}, connections)
		toggle = not toggle
		go = false
	end
	if not love.keyboard.isDown('o') then

		go = true
	end
	if love.keyboard.isDown('r') then
		start, finish, connections = mazeGenerate(height, width)
	end
end

function love.draw()
	
	local size = 500 / ((height + width) / 2)
	love.graphics.setColor(255, 255, 255)
	for i,v in ipairs(connections) do
		local distancex = v.x2 - v.x
		local distancey = v.y2 - v.y
		if distancex == 0 then distancex = 0.8 end
		if distancey == 0 then distancey = 0.8 end
		love.graphics.rectangle('fill', v.x * size, v.y * size, distancex * size, distancey * size)
	end
	
	for i=1, #grid do
		for o=1, #grid[i] do
			if ((i == start[2]) and (o == start[1])) then
				love.graphics.setColor(0, 255, 0)
			elseif ((i == finish[2]) and (o == finish[1])) then
				love.graphics.setColor(255, 0, 0)
			else
				love.graphics.setColor(255, 255, 255)
			end
			love.graphics.rectangle('fill', o * size, i * size, size * 0.8, size * 0.8)
			--love.graphics.setColor(0, 0, 0)
			--love.graphics.print(o.." "..i, o * size, i * size)
		end
	end
	for i,v in ipairs(connectionPath) do
		love.graphics.setColor(0, 128, 255)
		local x
		local y
		local distancex
		local distancey
		x = v.x2 + (v.x - v.x2)
		y = v.y2 + (v.y - v.y2)
		distancex = math.sqrt((v.x2 - v.x)^2)
		distancey = math.sqrt((v.y2 - v.y)^2)
		if v.x2 < v.x then x = x - 0.2 end
		if v.y2 < v.y then y = y - 0.2 end
		if distancex == 0 then distancex = 0.8 end
		if distancey == 0 then distancey = 0.8 end
		if toggle then
			love.graphics.rectangle('fill', x * size, y * size, distancex * size, distancey * size)
		end
	end
end

function mazeGenerate(heightg, widthg)
	local finished = false
	local cx = math.random(1, widthg)
	local cy = math.random(1, heightg)
	local startg = {cx, cy}
	local ncx = 1
	local ncy = 1
	local done = {}
	local divides = {}
	local connections = {}
	local divide = 0
	local directions = {"u", "r", "d", "l"}
	while not finished do
		divide = 0
		local location = {x = cx, y = cy}
		table.insert(done, location)
		for i,v in ipairs(directions) do
			local placeholder = v
			local s = math.random(1, #directions)
			directions[i] = directions[s]
			directions[s] = v
		end
		
		for i,v in ipairs(directions) do
			local valid = true
			local nx = cx
			local ny = cy
			if v == "u" then
				ny = ny - 1
			end
			if v == "r" then
				nx = nx + 1
			end
			if v == "d" then
				ny = ny + 1
			end
			if v == "l" then
				nx = nx - 1
			end
			
			if (nx < 1 or nx > widthg) or (ny < 1 or ny > heightg) then
				valid = false
			end
			for o,c in ipairs(done) do
				if (c.y == ny) and (c.x == nx) then
					valid = false
				end
			end
			if valid then
				if divide == 0 then
					ncx = nx
					ncy = ny
					local location2 = {x = ncx, y = ncy}
					table.insert(divides, 1, location2)
				end
				divide = divide + 1
			end
		end
		if divide >= 2 then
			table.insert(divides, 1, location)
		end
		if divide == 0 then
			cx = divides[1].x
			cy = divides[1].y
			table.remove(divides, 1)
		end
		if divide >= 1 then
			local connection = {x = cx, y = cy, x2 = ncx, y2 = ncy}
			table.insert(connections, connection)
			cx = ncx
			cy = ncy
		end
		if #connections == heightg * widthg - 1 then
			finished = true
		end
	end
	local finishg = {cx, cy}
	return startg, finishg, connections
end

function mazeSolve(start, finish, connections)
	local cx = start[1]
	local cy = start[2]
	local endx = finish[1]
	local endy = finish[2]
	local done = {}
	local divides = {}
	local finished = false
	local connectionPath = {}
	local currentC = {}
	local timer = {{}}
	while not finished do
		currentC = {}
		for i,v in ipairs(connections) do
			if v.x == cx and v.y == cy then
				local valid = true
				for o,c in ipairs(done) do
					if (c.x == v.x2) and (c.y == v.y2) then
						valid = false
					end
				end
				if valid then
					local Sq = {x = v.x2, y = v.y2}
					table.insert(currentC, Sq)
				end
			end
			if v.x2 == cx and v.y2 == cy then
				local valid = true
				for o,c in ipairs(done) do
					if (c.x == v.x) and (c.y == v.y) then
						valid = false
					end
				end
				if valid then
					local Sq = {x = v.x, y = v.y}
					table.insert(currentC, Sq)
				end
			end
		end
		local location = {x = cx, y = cy}	
		table.insert(done, location)
		if #currentC >= 2 then
			table.insert(divides, 1, location)
			table.insert(timer, 1, {})
		end
		if cx == endx and cy == endy then
			finished = true
			table.insert(timer[1], {x = location.x, y = location.y, x2 = cx, y2 = cy})
		elseif #currentC == 0 then
			cx = divides[1].x
			cy = divides[1].y
			table.remove(timer, 1)
			table.remove(divides, 1)
		end
		
		if #currentC >= 1 then
			rand = math.random(1, #currentC)
			cx = currentC[rand].x
			cy = currentC[rand].y
			table.insert(timer[1], {x = location.x, y = location.y, x2 = cx, y2 = cy})
		end
		
	end
	for i,v in ipairs(timer) do
		for o,c in ipairs(v) do
			table.insert(connectionPath, c)
		end
	end
	return connectionPath
end








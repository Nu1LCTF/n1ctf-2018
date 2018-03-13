
CXXFLAGS := -std=c++11
CXX := g++
OBJS := main.o
TARGET := null
LDFLAGS := -lpthread -Wl,-z,relro,-z,now -D_FORTIFY_SOURCE=2
STRIP := strip
STRIPFLAGS := --strip-all

all: $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LDFLAGS)
	$(STRIP) $(STRIPFLAGS) $(TARGET)

clean:
	rm -f $(TARGET) $(OBJS)

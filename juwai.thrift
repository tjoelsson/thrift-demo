namespace php juwai
namespace py juwai

struct TProperty {
	1: i64 id,
	2: string description,
}

exception NoSuchObject {
	1: string message,
}

exception SelectFailed {
	1: string message,
}

exception InsertFailed {
	1: string message,
}

service PropertyService
{
	TProperty getProperty(1:i64 id) throws (1:SelectFailed ex1, 2:NoSuchObject ex2),
	void addProperty(1:TProperty prop) throws (1:InsertFailed ex),
}

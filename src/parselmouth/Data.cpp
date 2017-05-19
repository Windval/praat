#include "Parselmouth.h"

namespace py = pybind11;
using namespace py::literals;

namespace parselmouth {

void initData(PraatBindings &bindings)
{
	bindings.get<Data>()

			//.def_static("read", // TODO Praat-format files not recognized because we cannot call praat_uvafon_init because INCLUDE_MANPAGES cannot be used because somehow that's not supposed to be called after only praatlib_init() instead of praat_init()
			//            [] (const std::string &filePath) { // TODO std::string to MelderFile functionality in separate function? Cfr. Sound.__init__
			//	            structMelderFile file = {};
			//	            Melder_relativePathToFile(Melder_peek8to32(filePath.c_str()), &file);
			//	            return Data_readFromFile(&file);
			//            },
			//            "file_path"_a)

			.def("copy",
				 &Data_copy<structData>)

			.def("__copy__",
			     &Data_copy<structData>)

			.def("__deepcopy__",
			     &Data_copy<structData>)

			;
}

} // namespace parselmouth

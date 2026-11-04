
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue,mergeSlotProps,refs} from "$/utils/state"
import {Box as RadixThemesBox,Button as RadixThemesButton,Flex as RadixThemesFlex,Select as RadixThemesSelect,Text as RadixThemesText,TextArea as RadixThemesTextArea,TextField as RadixThemesTextField} from "@radix-ui/themes"
import {UploadFilesContext,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect,useRef} from "react"
import {jsx} from "@emotion/react"
import {useStateContext} from "$/utils/context-registry"
import {} from "react-dropzone"
import {useDropzone} from "react-dropzone"
import DebounceInput from "react-debounce-input"








export const Button_button_ce1f76161399883ad9e25c58dccd4ffa_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_ce1f76161399883ad9e25c58dccd4ffa_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_791672e8a7a06c8222ff645442dda0c6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "numpy" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_791672e8a7a06c8222ff645442dda0c6 }))},children)
    )
});
Button_button_ce1f76161399883ad9e25c58dccd4ffa_66aa3b90.displayName = "Button";
return Button_button_ce1f76161399883ad9e25c58dccd4ffa_66aa3b90;
})();

export const Button_button_697f0f56d01a5d0d08106dbadb644c46_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_697f0f56d01a5d0d08106dbadb644c46_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_079f1253573c23e804ef9ab4ae493922 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "pandas" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_079f1253573c23e804ef9ab4ae493922 }))},children)
    )
});
Button_button_697f0f56d01a5d0d08106dbadb644c46_66aa3b90.displayName = "Button";
return Button_button_697f0f56d01a5d0d08106dbadb644c46_66aa3b90;
})();

export const Button_button_00639f932bf836285537da1a1bbfc611_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_00639f932bf836285537da1a1bbfc611_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_c975f32d876cddfbc88a72e061d1f56a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "matplotlib" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_c975f32d876cddfbc88a72e061d1f56a }))},children)
    )
});
Button_button_00639f932bf836285537da1a1bbfc611_66aa3b90.displayName = "Button";
return Button_button_00639f932bf836285537da1a1bbfc611_66aa3b90;
})();

export const Button_button_f86790f043dda989e0c27dd9b2a3c36e_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_f86790f043dda989e0c27dd9b2a3c36e_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_e1400e4bd8c31922695cde246e18785a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "seaborn" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_e1400e4bd8c31922695cde246e18785a }))},children)
    )
});
Button_button_f86790f043dda989e0c27dd9b2a3c36e_66aa3b90.displayName = "Button";
return Button_button_f86790f043dda989e0c27dd9b2a3c36e_66aa3b90;
})();

export const Button_button_e7cfea85af571847d94dc5aa9dedf40f_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_e7cfea85af571847d94dc5aa9dedf40f_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_3a7dd40b050d0835ffd6b7fe99f3fc12 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "sklearn" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_3a7dd40b050d0835ffd6b7fe99f3fc12 }))},children)
    )
});
Button_button_e7cfea85af571847d94dc5aa9dedf40f_66aa3b90.displayName = "Button";
return Button_button_e7cfea85af571847d94dc5aa9dedf40f_66aa3b90;
})();

export const Button_button_b5575478594af6ab2cd906a710cdfbe4_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_b5575478594af6ab2cd906a710cdfbe4_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_818f1c5c61d84492101c741bb804ca3a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "torch" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_818f1c5c61d84492101c741bb804ca3a }))},children)
    )
});
Button_button_b5575478594af6ab2cd906a710cdfbe4_66aa3b90.displayName = "Button";
return Button_button_b5575478594af6ab2cd906a710cdfbe4_66aa3b90;
})();

export const Button_button_a69ae905019e323c127ca23066d87e7c_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_a69ae905019e323c127ca23066d87e7c_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_5bec0f8897a5068ce9a32a24a1035a2b = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "tensorflow" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_5bec0f8897a5068ce9a32a24a1035a2b }))},children)
    )
});
Button_button_a69ae905019e323c127ca23066d87e7c_66aa3b90.displayName = "Button";
return Button_button_a69ae905019e323c127ca23066d87e7c_66aa3b90;
})();

export const Bare_comp_5ab6f538659d533714715a63cb92d666_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_5ab6f538659d533714715a63cb92d666_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.initials_rx_state_
    )
});
Bare_comp_5ab6f538659d533714715a63cb92d666_66aa3b90.displayName = "Bare";
return Bare_comp_5ab6f538659d533714715a63cb92d666_66aa3b90;
})();

export const Box_box_c22865b79f321cbc36a1b8dbd5f84564_66aa3b90 = /*#__PURE__*/ (() => {
const Box_box_c22865b79f321cbc36a1b8dbd5f84564_66aa3b90 = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(RadixThemesBox,{...mergeSlotProps(rest, ({ css:({ ["background"] : reflex___state____state__reflexsqlite___state___base____auth_state.avatar_color_rx_state_, ["borderRadius"] : "999px", ["width"] : "32px", ["height"] : "32px", ["minWidth"] : "32px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" }) }))},children)
    )
});
Box_box_c22865b79f321cbc36a1b8dbd5f84564_66aa3b90.displayName = "Box";
return Box_box_c22865b79f321cbc36a1b8dbd5f84564_66aa3b90;
})();

export const Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.display_name_rx_state_
    )
});
Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_66aa3b90.displayName = "Bare";
return Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_66aa3b90;
})();

export const Bare_comp_bcff288a0ef24fc2c402098247cbd23b_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_bcff288a0ef24fc2c402098247cbd23b_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.role_rx_state_
    )
});
Bare_comp_bcff288a0ef24fc2c402098247cbd23b_66aa3b90.displayName = "Bare";
return Bare_comp_bcff288a0ef24fc2c402098247cbd23b_66aa3b90;
})();

export const Button_button_f9de5aac8983a4287e20b52d3112c0ce_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_f9de5aac8983a4287e20b52d3112c0ce_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_42b68d07de6d2f872f818321f5b24e9f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.sign_out", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_42b68d07de6d2f872f818321f5b24e9f }))},children)
    )
});
Button_button_f9de5aac8983a4287e20b52d3112c0ce_66aa3b90.displayName = "Button";
return Button_button_f9de5aac8983a4287e20b52d3112c0ce_66aa3b90;
})();

export const Styledupload_comp_3412be2145c666ecee0caa1db7ff10b9_66aa3b90 = /*#__PURE__*/ (() => {
const Styledupload_comp_3412be2145c666ecee0caa1db7ff10b9_66aa3b90 = memo(({children}) => {
    const ref_dataset_upload = useRef(null); refs["ref_dataset_upload"] = ref_dataset_upload;
const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_drop_cf490c5e113076e2667aca0fe89f369f = useCallback(((_ev_0) => ((e => setFilesById(filesById => {
    const updatedFilesById = Object.assign({}, filesById);
    updatedFilesById["dataset_upload"] = e;
    return updatedFilesById;
  })
    )(_ev_0))), [addEvents, ReflexEvent, filesById, setFilesById])
const on_drop_rejected_2fcedbdc0771e7617b4270e2d1ac8cc9 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => (refs['__toast']?.["error"]("", ({ ["title"] : "Files not Accepted", ["description"] : _ev_0.map(((osizayzf) => (osizayzf?.["file"]?.["path"]+": "+osizayzf?.["errors"].map(((wnkiegyk) => wnkiegyk?.["message"])).join(", ")))).join("\n\n"), ["closeButton"] : true, ["style"] : ({ ["whiteSpace"] : "pre-line" }) })))), ["callback"] : null }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const { getRootProps: xdvxrcsn, getInputProps: udaxihhe, isDragActive: bacghqta} = useDropzone(({ ["multiple"] : true, ["id"] : "dataset_upload", ["onDrop"] : on_drop_cf490c5e113076e2667aca0fe89f369f, ["onDropRejected"] : on_drop_rejected_2fcedbdc0771e7617b4270e2d1ac8cc9 }));
    return(
        jsx(Fragment,{},jsx("div",{className:"rx-Upload",css:({ ["border"] : "2px dashed #C7D2FE", ["borderRadius"] : "12px", ["background"] : "#EEF0FF", ["width"] : "100%", ["padding"] : "6px", ["textAlign"] : "center" }),id:"dataset_upload",ref:ref_dataset_upload,...xdvxrcsn()},jsx("input",{type:"file",...udaxihhe()},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "8px", ["alignItems"] : "center", ["padding"] : "18px" }),direction:"column",gap:"3"},jsx(RadixThemesBox,{css:({ ["background"] : "#4F46E5", ["borderRadius"] : "10px", ["width"] : "38px", ["height"] : "38px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" })},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "13px", ["fontWeight"] : "800", ["color"] : "white" })},"UP")),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "12px", ["fontWeight"] : "600", ["color"] : "#111827" })},"Drop a file here or click to browse"),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B" })},"Maximum 25 MB \u00b7 headers are read automatically"))))
    )
});
Styledupload_comp_3412be2145c666ecee0caa1db7ff10b9_66aa3b90.displayName = "StyledUpload";
return Styledupload_comp_3412be2145c666ecee0caa1db7ff10b9_66aa3b90;
})();

export const Debounceinput_debounceinput_8e608835f3a27aa208b0ed024c30b8b5_66aa3b90 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_8e608835f3a27aa208b0ed024c30b8b5_66aa3b90 = memo(({children, ...rest}) => {
    const on_change_2c4df6f6ccf7f9ef5271c580177b49f8 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.set_upload_description", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_2c4df6f6ccf7f9ef5271c580177b49f8, placeholder:"What is this dataset about?", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.upload_description_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.upload_description_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_8e608835f3a27aa208b0ed024c30b8b5_66aa3b90.displayName = "DebounceInput";
return Debounceinput_debounceinput_8e608835f3a27aa208b0ed024c30b8b5_66aa3b90;
})();

export const Button_button_2c95d5176feec05df11faedb643c86e0_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_2c95d5176feec05df11faedb643c86e0_66aa3b90 = memo(({children, ...rest}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_click_a73228434cccbabf8f90051000a70362 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.handle_upload", ({ ["files"] : filesById?.["dataset_upload"], ["upload_param_name"] : "files", ["upload_id"] : "dataset_upload", ["extra_headers"] : ({  }) }), ({  }), "uploadFiles"))], [_e], ({  })))), [addEvents, ReflexEvent, filesById, setFilesById])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }), ["width"] : "100%" }), disabled:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.is_uploading_rx_state_, onClick:on_click_a73228434cccbabf8f90051000a70362 }))},children)
    )
});
Button_button_2c95d5176feec05df11faedb643c86e0_66aa3b90.displayName = "Button";
return Button_button_2c95d5176feec05df11faedb643c86e0_66aa3b90;
})();

export const Bare_comp_08cd8ebf346b93a31b09fff537bebd98_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_08cd8ebf346b93a31b09fff537bebd98_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.upload_message_rx_state_
    )
});
Bare_comp_08cd8ebf346b93a31b09fff537bebd98_66aa3b90.displayName = "Bare";
return Bare_comp_08cd8ebf346b93a31b09fff537bebd98_66aa3b90;
})();

export const Cond_comp_da0294a4e611df75bf17f0f22d7c5771_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_da0294a4e611df75bf17f0f22d7c5771_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.upload_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_da0294a4e611df75bf17f0f22d7c5771_66aa3b90.displayName = "Cond";
return Cond_comp_da0294a4e611df75bf17f0f22d7c5771_66aa3b90;
})();

export const Bare_comp_5a8a7d2dad3092f0aaac7dd41ed88b76_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_5a8a7d2dad3092f0aaac7dd41ed88b76_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.upload_error_rx_state_
    )
});
Bare_comp_5a8a7d2dad3092f0aaac7dd41ed88b76_66aa3b90.displayName = "Bare";
return Bare_comp_5a8a7d2dad3092f0aaac7dd41ed88b76_66aa3b90;
})();

export const Cond_comp_2ba8d579ef5127d94464328f8d17d4c8_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_2ba8d579ef5127d94464328f8d17d4c8_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.upload_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_2ba8d579ef5127d94464328f8d17d4c8_66aa3b90.displayName = "Cond";
return Cond_comp_2ba8d579ef5127d94464328f8d17d4c8_66aa3b90;
})();

export const Debounceinput_debounceinput_3e89c6c638653ab7dedebc1e0cb68068_66aa3b90 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_3e89c6c638653ab7dedebc1e0cb68068_66aa3b90 = memo(({children, ...rest}) => {
    const on_change_c7a8b1d4a9c04cf47c36f4bd1a4c71e8 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.set_dataset_search", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_c7a8b1d4a9c04cf47c36f4bd1a4c71e8, placeholder:"Search datasets by name or filename", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.dataset_search_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.dataset_search_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_3e89c6c638653ab7dedebc1e0cb68068_66aa3b90.displayName = "DebounceInput";
return Debounceinput_debounceinput_3e89c6c638653ab7dedebc1e0cb68068_66aa3b90;
})();

export const Foreach_comp_bc06564eb99827015c14a9618f57216f_66aa3b90 = /*#__PURE__*/ (() => {
const Foreach_comp_bc06564eb99827015c14a9618f57216f_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.datasets_rx_state_ ?? [],((item_rx_state_,index_d9c139ef9274834cecd83063127db4e6)=>(jsx(RadixThemesButton,{css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "12px", ["padding"] : "14px", ["cursor"] : "pointer", ["width"] : "230px", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #C7D2FE" }) }),key:index_d9c139ef9274834cecd83063127db4e6,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.select_dataset", ({ ["dataset_id"] : item_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "6px", ["alignItems"] : "start", ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(RadixThemesBox,{css:({ ["background"] : "#EEF0FF", ["border"] : "1px solid #DDD6FE", ["borderRadius"] : "999px", ["padding"] : "3px 10px", ["whiteSpace"] : "nowrap" })},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["fontWeight"] : "600", ["color"] : "#4F46E5" })},item_rx_state_?.["format"])),jsx(RadixThemesBox,{css:({ ["flex"] : "1" })},),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "9px", ["color"] : "#94A3B8" })},item_rx_state_?.["updated"])),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "13px", ["fontWeight"] : "700", ["color"] : "#111827", ["textAlign"] : "left", ["width"] : "100%" })},item_rx_state_?.["name"]),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B", ["textAlign"] : "left", ["width"] : "100%" })},item_rx_state_?.["description"]),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "12px", ["width"] : "100%" }),direction:"row",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B" })},(item_rx_state_?.["rows"]+" rows")),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B" })},(item_rx_state_?.["columns"]+" cols")),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B" })},(item_rx_state_?.["size_kb"]+" KB"))))))))
    )
});
Foreach_comp_bc06564eb99827015c14a9618f57216f_66aa3b90.displayName = "Foreach";
return Foreach_comp_bc06564eb99827015c14a9618f57216f_66aa3b90;
})();

export const Bare_comp_a4f1a15ac5587d6c7292d8e5466bf396_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_a4f1a15ac5587d6c7292d8e5466bf396_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.active_name_rx_state_
    )
});
Bare_comp_a4f1a15ac5587d6c7292d8e5466bf396_66aa3b90.displayName = "Bare";
return Bare_comp_a4f1a15ac5587d6c7292d8e5466bf396_66aa3b90;
})();

export const Button_button_b2597bc44389bd8a58bf34da34aa35d8_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_b2597bc44389bd8a58bf34da34aa35d8_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_dfd6a6bac15582b6883af8760d321682 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.open_meta", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_dfd6a6bac15582b6883af8760d321682 }))},children)
    )
});
Button_button_b2597bc44389bd8a58bf34da34aa35d8_66aa3b90.displayName = "Button";
return Button_button_b2597bc44389bd8a58bf34da34aa35d8_66aa3b90;
})();

export const Button_button_b7a4ec60e3d03d44edbc027f5e32bb7a_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_b7a4ec60e3d03d44edbc027f5e32bb7a_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_57eb4e212f154f5a3bd8cfd7499a63d3 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.download_csv", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_57eb4e212f154f5a3bd8cfd7499a63d3 }))},children)
    )
});
Button_button_b7a4ec60e3d03d44edbc027f5e32bb7a_66aa3b90.displayName = "Button";
return Button_button_b7a4ec60e3d03d44edbc027f5e32bb7a_66aa3b90;
})();

export const Button_button_46a47dfd4fe8022ecb5b01fda7f09866_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_46a47dfd4fe8022ecb5b01fda7f09866_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_1f3e08f6b707df9e63c558a6be0d3bcb = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.delete_dataset", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FEF2F2", ["color"] : "#EF4444", ["border"] : "1px solid #FECACA", ["borderRadius"] : "9px", ["padding"] : "8px 13px", ["fontSize"] : "12px", ["fontWeight"] : "600", ["cursor"] : "pointer" }), onClick:on_click_1f3e08f6b707df9e63c558a6be0d3bcb }))},children)
    )
});
Button_button_46a47dfd4fe8022ecb5b01fda7f09866_66aa3b90.displayName = "Button";
return Button_button_46a47dfd4fe8022ecb5b01fda7f09866_66aa3b90;
})();

export const Button_button_1b0551fca0c50b49d26604cdb176e82c_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_1b0551fca0c50b49d26604cdb176e82c_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_e4d2b0d69af3af8892d82b7e227548ec = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.open_add", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }) }), onClick:on_click_e4d2b0d69af3af8892d82b7e227548ec }))},children)
    )
});
Button_button_1b0551fca0c50b49d26604cdb176e82c_66aa3b90.displayName = "Button";
return Button_button_1b0551fca0c50b49d26604cdb176e82c_66aa3b90;
})();

export const Debounceinput_debounceinput_8f0447767e11d95e4f0a420ad65893c9_66aa3b90 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_8f0447767e11d95e4f0a420ad65893c9_66aa3b90 = memo(({children, ...rest}) => {
    const on_change_1fca951678c93665b5d457a9f3494bdf = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.set_row_search", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_1fca951678c93665b5d457a9f3494bdf, placeholder:"Search rows...", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.row_search_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.row_search_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_8f0447767e11d95e4f0a420ad65893c9_66aa3b90.displayName = "DebounceInput";
return Debounceinput_debounceinput_8f0447767e11d95e4f0a420ad65893c9_66aa3b90;
})();

export const Selectroot_select__root_cbc59d27b3dbe0042b5643f5b24c56cf_66aa3b90 = /*#__PURE__*/ (() => {
const Selectroot_select__root_cbc59d27b3dbe0042b5643f5b24c56cf_66aa3b90 = memo(({children, ...rest}) => {
    const on_change_2584b8098dfe88912cd38055ec24bf6b = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.set_page_size", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesSelect.Root,{...mergeSlotProps(rest, ({ onValueChange:on_change_2584b8098dfe88912cd38055ec24bf6b, size:"1", value:"10" }))},children)
    )
});
Selectroot_select__root_cbc59d27b3dbe0042b5643f5b24c56cf_66aa3b90.displayName = "SelectRoot";
return Selectroot_select__root_cbc59d27b3dbe0042b5643f5b24c56cf_66aa3b90;
})();

export const Foreach_comp_c8ffb2523d21fc3ec859e2e321dbf920_66aa3b90 = /*#__PURE__*/ (() => {
const Foreach_comp_c8ffb2523d21fc3ec859e2e321dbf920_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.columns_rx_state_ ?? [],((col_rx_state_,index_fb0574821ac14a94164c40ce54e03fa9)=>(jsx(RadixThemesBox,{css:({ ["minWidth"] : "128px", ["flex"] : "1", ["padding"] : "10px 8px" }),key:index_fb0574821ac14a94164c40ce54e03fa9},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["fontWeight"] : "700", ["color"] : "#64748B", ["whiteSpace"] : "nowrap" })},col_rx_state_)))))
    )
});
Foreach_comp_c8ffb2523d21fc3ec859e2e321dbf920_66aa3b90.displayName = "Foreach";
return Foreach_comp_c8ffb2523d21fc3ec859e2e321dbf920_66aa3b90;
})();

export const Foreach_comp_02ca13566328b201f95280d830a633ba_66aa3b90 = /*#__PURE__*/ (() => {
const Foreach_comp_02ca13566328b201f95280d830a633ba_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.table_rows_rx_state_ ?? [],((item_rx_state_,index_64e7f345df615794889921f8b59c1b04)=>(jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["borderBottom"] : "1px solid #E5E8F1", ["gap"] : "0", ["&:hover"] : ({ ["background"] : "#FAFBFE" }), ["alignItems"] : "center" }),direction:"row",key:index_64e7f345df615794889921f8b59c1b04,gap:"3"},jsx(RadixThemesBox,{css:({ ["width"] : "48px", ["minWidth"] : "48px", ["padding"] : "10px 8px" })},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["color"] : "#94A3B8" })},item_rx_state_?.["_index"])),Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.columns_rx_state_ ?? [],((col_rx_state_,index_ed32ac638a876b8e70d666686dfcdef9)=>(jsx(RadixThemesBox,{css:({ ["minWidth"] : "128px", ["flex"] : "1", ["padding"] : "10px 8px", ["overflow"] : "hidden" }),key:index_ed32ac638a876b8e70d666686dfcdef9},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "12px", ["color"] : "#111827", ["whiteSpace"] : "nowrap" })},item_rx_state_?.[col_rx_state_]))))),jsx(RadixThemesBox,{css:({ ["width"] : "118px", ["minWidth"] : "118px", ["padding"] : "8px" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "6px" }),direction:"row",gap:"3"},jsx(RadixThemesButton,{css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "5px 9px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.open_edit", ({ ["row_id"] : item_rx_state_?.["_id"] }), ({  })))], [_e], ({  }))))},"Edit"),jsx(RadixThemesButton,{css:({ ["background"] : "#FEF2F2", ["color"] : "#EF4444", ["border"] : "1px solid #FECACA", ["borderRadius"] : "9px", ["padding"] : "5px 9px", ["fontSize"] : "12px", ["fontWeight"] : "600", ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.delete_row", ({ ["row_id"] : item_rx_state_?.["_id"] }), ({  })))], [_e], ({  }))))},"Delete")))))))
    )
});
Foreach_comp_02ca13566328b201f95280d830a633ba_66aa3b90.displayName = "Foreach";
return Foreach_comp_02ca13566328b201f95280d830a633ba_66aa3b90;
})();

export const Cond_comp_db926e192ee3210e931a40316c9bc5d5_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_db926e192ee3210e931a40316c9bc5d5_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.has_datasets_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_db926e192ee3210e931a40316c9bc5d5_66aa3b90.displayName = "Cond";
return Cond_comp_db926e192ee3210e931a40316c9bc5d5_66aa3b90;
})();

export const Bare_comp_0a3164719369b8ee35a84c5254e9fa31_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_0a3164719369b8ee35a84c5254e9fa31_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.total_rows_rx_state_
    )
});
Bare_comp_0a3164719369b8ee35a84c5254e9fa31_66aa3b90.displayName = "Bare";
return Bare_comp_0a3164719369b8ee35a84c5254e9fa31_66aa3b90;
})();

export const Button_button_3cbb8f736cee8cef193fb876bae0f229_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_3cbb8f736cee8cef193fb876bae0f229_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_e06bc33caa0c87d825eb993d42bd93a0 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.prev_page", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_e06bc33caa0c87d825eb993d42bd93a0 }))},children)
    )
});
Button_button_3cbb8f736cee8cef193fb876bae0f229_66aa3b90.displayName = "Button";
return Button_button_3cbb8f736cee8cef193fb876bae0f229_66aa3b90;
})();

export const Bare_comp_3ed5d821564bd828695a5afedab35139_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_3ed5d821564bd828695a5afedab35139_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.page_rx_state_
    )
});
Bare_comp_3ed5d821564bd828695a5afedab35139_66aa3b90.displayName = "Bare";
return Bare_comp_3ed5d821564bd828695a5afedab35139_66aa3b90;
})();

export const Bare_comp_d507bc9adff48022bc6a61690d65866d_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_d507bc9adff48022bc6a61690d65866d_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.page_count_rx_state_
    )
});
Bare_comp_d507bc9adff48022bc6a61690d65866d_66aa3b90.displayName = "Bare";
return Bare_comp_d507bc9adff48022bc6a61690d65866d_66aa3b90;
})();

export const Button_button_8decbad6ca03843fb470aefdd7d1a676_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_8decbad6ca03843fb470aefdd7d1a676_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_c3f10ee3f21e2702943426799d8031a3 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.next_page", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_c3f10ee3f21e2702943426799d8031a3 }))},children)
    )
});
Button_button_8decbad6ca03843fb470aefdd7d1a676_66aa3b90.displayName = "Button";
return Button_button_8decbad6ca03843fb470aefdd7d1a676_66aa3b90;
})();

export const Bare_comp_c5cf5580afeccbe4461f23d42dd463b5_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_c5cf5580afeccbe4461f23d42dd463b5_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.notice_rx_state_
    )
});
Bare_comp_c5cf5580afeccbe4461f23d42dd463b5_66aa3b90.displayName = "Bare";
return Bare_comp_c5cf5580afeccbe4461f23d42dd463b5_66aa3b90;
})();

export const Cond_comp_df45ff915c5f4036877597b29bf78fec_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_df45ff915c5f4036877597b29bf78fec_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_df45ff915c5f4036877597b29bf78fec_66aa3b90.displayName = "Cond";
return Cond_comp_df45ff915c5f4036877597b29bf78fec_66aa3b90;
})();

export const Bare_comp_63a023bc5b1f66881bfe3848351084af_66aa3b90 = /*#__PURE__*/ (() => {
const Bare_comp_63a023bc5b1f66881bfe3848351084af_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.error_rx_state_
    )
});
Bare_comp_63a023bc5b1f66881bfe3848351084af_66aa3b90.displayName = "Bare";
return Bare_comp_63a023bc5b1f66881bfe3848351084af_66aa3b90;
})();

export const Cond_comp_127bb22752bc75bbb4e18e5796301b77_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_127bb22752bc75bbb4e18e5796301b77_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_127bb22752bc75bbb4e18e5796301b77_66aa3b90.displayName = "Cond";
return Cond_comp_127bb22752bc75bbb4e18e5796301b77_66aa3b90;
})();

export const Foreach_comp_efb3ba22c377a153d1799a24694d78ca_66aa3b90 = /*#__PURE__*/ (() => {
const Foreach_comp_efb3ba22c377a153d1799a24694d78ca_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.columns_rx_state_ ?? [],((column_rx_state_,index_5835f5474d92147e811c16896bfd65fe)=>(jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "6px", ["alignItems"] : "start", ["width"] : "100%" }),direction:"column",key:index_5835f5474d92147e811c16896bfd65fe,gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "12px", ["fontWeight"] : "600", ["color"] : "#111827" })},column_rx_state_),jsx(DebounceInput,{css:({ ["width"] : "100%", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 11px", ["fontSize"] : "12px" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.set_form_field", ({ ["key"] : column_rx_state_, ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))),placeholder:("Value for "+column_rx_state_),value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.form_values_rx_state_?.[column_rx_state_]) ? reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.form_values_rx_state_?.[column_rx_state_] : "")},),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["color"] : "#94A3B8" })},"")))))
    )
});
Foreach_comp_efb3ba22c377a153d1799a24694d78ca_66aa3b90.displayName = "Foreach";
return Foreach_comp_efb3ba22c377a153d1799a24694d78ca_66aa3b90;
})();

export const Button_button_9c5b85d296db348fa0d4f30df69d76c1_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_9c5b85d296db348fa0d4f30df69d76c1_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_63a7ee0057ee83814464e1966078e3fd = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.save_new_row", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }) }), onClick:on_click_63a7ee0057ee83814464e1966078e3fd }))},children)
    )
});
Button_button_9c5b85d296db348fa0d4f30df69d76c1_66aa3b90.displayName = "Button";
return Button_button_9c5b85d296db348fa0d4f30df69d76c1_66aa3b90;
})();

export const Button_button_1f2d9c776433a1c6705449c815da25c1_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_1f2d9c776433a1c6705449c815da25c1_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_72ec739bfabf89a58484e250ef356fea = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.close_dialogs", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_72ec739bfabf89a58484e250ef356fea }))},children)
    )
});
Button_button_1f2d9c776433a1c6705449c815da25c1_66aa3b90.displayName = "Button";
return Button_button_1f2d9c776433a1c6705449c815da25c1_66aa3b90;
})();

export const Cond_comp_25198a814f4a55d89c34f8d605a8c5d7_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_25198a814f4a55d89c34f8d605a8c5d7_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.show_add_dialog_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_25198a814f4a55d89c34f8d605a8c5d7_66aa3b90.displayName = "Cond";
return Cond_comp_25198a814f4a55d89c34f8d605a8c5d7_66aa3b90;
})();

export const Button_button_c3e34dfa615dad75b8b26c3bd554874e_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_c3e34dfa615dad75b8b26c3bd554874e_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_06e5a5c4d2fbd2b77aadce5d97a63041 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.save_edited_row", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }) }), onClick:on_click_06e5a5c4d2fbd2b77aadce5d97a63041 }))},children)
    )
});
Button_button_c3e34dfa615dad75b8b26c3bd554874e_66aa3b90.displayName = "Button";
return Button_button_c3e34dfa615dad75b8b26c3bd554874e_66aa3b90;
})();

export const Cond_comp_4bc26453a4e7c4cbe38a01bc0eec2db3_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_4bc26453a4e7c4cbe38a01bc0eec2db3_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.show_edit_dialog_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_4bc26453a4e7c4cbe38a01bc0eec2db3_66aa3b90.displayName = "Cond";
return Cond_comp_4bc26453a4e7c4cbe38a01bc0eec2db3_66aa3b90;
})();

export const Debounceinput_debounceinput_40228ed08645178f98e7fa2376e55a5a_66aa3b90 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_40228ed08645178f98e7fa2376e55a5a_66aa3b90 = memo(({children, ...rest}) => {
    const on_change_e91fe2b0d2c2b8a720d5020ff6bdd21a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.set_meta_name", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_e91fe2b0d2c2b8a720d5020ff6bdd21a, placeholder:"Dataset name", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.meta_name_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.meta_name_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_40228ed08645178f98e7fa2376e55a5a_66aa3b90.displayName = "DebounceInput";
return Debounceinput_debounceinput_40228ed08645178f98e7fa2376e55a5a_66aa3b90;
})();

export const Debounceinput_debounceinput_10e03c4fdabb875c409d836823cf47bf_66aa3b90 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_10e03c4fdabb875c409d836823cf47bf_66aa3b90 = memo(({children, ...rest}) => {
    const on_change_3f7ecfd40def312dcabd5f97f25279d1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.set_meta_description", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["minHeight"] : "90px", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "12px" }), debounceTimeout:300, element:RadixThemesTextArea, onChange:on_change_3f7ecfd40def312dcabd5f97f25279d1, placeholder:"Describe this dataset", value:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.meta_description_rx_state_ }), "inputRef")},)
    )
});
Debounceinput_debounceinput_10e03c4fdabb875c409d836823cf47bf_66aa3b90.displayName = "DebounceInput";
return Debounceinput_debounceinput_10e03c4fdabb875c409d836823cf47bf_66aa3b90;
})();

export const Button_button_29a9c42a8906976b301e296c9f3b6f8b_66aa3b90 = /*#__PURE__*/ (() => {
const Button_button_29a9c42a8906976b301e296c9f3b6f8b_66aa3b90 = memo(({children, ...rest}) => {
    const on_click_d80b4fb00126a8233bf86541a5b187dc = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state.save_metadata", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }) }), onClick:on_click_d80b4fb00126a8233bf86541a5b187dc }))},children)
    )
});
Button_button_29a9c42a8906976b301e296c9f3b6f8b_66aa3b90.displayName = "Button";
return Button_button_29a9c42a8906976b301e296c9f3b6f8b_66aa3b90;
})();

export const Cond_comp_96ede31fa39da3a1400acf1dcfede019_66aa3b90 = /*#__PURE__*/ (() => {
const Cond_comp_96ede31fa39da3a1400acf1dcfede019_66aa3b90 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dataset_state____dataset_state")
    return(
        (reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dataset_state____dataset_state.show_meta_dialog_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_96ede31fa39da3a1400acf1dcfede019_66aa3b90.displayName = "Cond";
return Cond_comp_96ede31fa39da3a1400acf1dcfede019_66aa3b90;
})();

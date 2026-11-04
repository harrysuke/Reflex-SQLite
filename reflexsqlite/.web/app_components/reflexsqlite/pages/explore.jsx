
import {ReflexEvent,applyEventActions,isTrue,mergeSlotProps} from "$/utils/state"
import {Box as RadixThemesBox,Button as RadixThemesButton,Flex as RadixThemesFlex,Select as RadixThemesSelect,Text as RadixThemesText} from "@radix-ui/themes"
import {ClientSide,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useEffect} from "react"
import {jsx} from "@emotion/react"
import {useStateContext} from "$/utils/context-registry"
import {Bar as RechartsBar,CartesianGrid as RechartsCartesianGrid,Line as RechartsLine,ResponsiveContainer as RechartsResponsiveContainer,Tooltip as RechartsTooltip,XAxis as RechartsXAxis,YAxis as RechartsYAxis} from "recharts"

const RechartsComposedChart = ClientSide(() => import('recharts').then((mod) => mod.ComposedChart), "RechartsComposedChart")






export const Button_button_ce1f76161399883ad9e25c58dccd4ffa_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_ce1f76161399883ad9e25c58dccd4ffa_cfd3635a = memo(({children, ...rest}) => {
    const on_click_791672e8a7a06c8222ff645442dda0c6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "numpy" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_791672e8a7a06c8222ff645442dda0c6 }))},children)
    )
});
Button_button_ce1f76161399883ad9e25c58dccd4ffa_cfd3635a.displayName = "Button";
return Button_button_ce1f76161399883ad9e25c58dccd4ffa_cfd3635a;
})();

export const Button_button_697f0f56d01a5d0d08106dbadb644c46_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_697f0f56d01a5d0d08106dbadb644c46_cfd3635a = memo(({children, ...rest}) => {
    const on_click_079f1253573c23e804ef9ab4ae493922 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "pandas" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_079f1253573c23e804ef9ab4ae493922 }))},children)
    )
});
Button_button_697f0f56d01a5d0d08106dbadb644c46_cfd3635a.displayName = "Button";
return Button_button_697f0f56d01a5d0d08106dbadb644c46_cfd3635a;
})();

export const Button_button_00639f932bf836285537da1a1bbfc611_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_00639f932bf836285537da1a1bbfc611_cfd3635a = memo(({children, ...rest}) => {
    const on_click_c975f32d876cddfbc88a72e061d1f56a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "matplotlib" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_c975f32d876cddfbc88a72e061d1f56a }))},children)
    )
});
Button_button_00639f932bf836285537da1a1bbfc611_cfd3635a.displayName = "Button";
return Button_button_00639f932bf836285537da1a1bbfc611_cfd3635a;
})();

export const Button_button_f86790f043dda989e0c27dd9b2a3c36e_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_f86790f043dda989e0c27dd9b2a3c36e_cfd3635a = memo(({children, ...rest}) => {
    const on_click_e1400e4bd8c31922695cde246e18785a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "seaborn" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_e1400e4bd8c31922695cde246e18785a }))},children)
    )
});
Button_button_f86790f043dda989e0c27dd9b2a3c36e_cfd3635a.displayName = "Button";
return Button_button_f86790f043dda989e0c27dd9b2a3c36e_cfd3635a;
})();

export const Button_button_e7cfea85af571847d94dc5aa9dedf40f_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_e7cfea85af571847d94dc5aa9dedf40f_cfd3635a = memo(({children, ...rest}) => {
    const on_click_3a7dd40b050d0835ffd6b7fe99f3fc12 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "sklearn" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_3a7dd40b050d0835ffd6b7fe99f3fc12 }))},children)
    )
});
Button_button_e7cfea85af571847d94dc5aa9dedf40f_cfd3635a.displayName = "Button";
return Button_button_e7cfea85af571847d94dc5aa9dedf40f_cfd3635a;
})();

export const Button_button_b5575478594af6ab2cd906a710cdfbe4_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_b5575478594af6ab2cd906a710cdfbe4_cfd3635a = memo(({children, ...rest}) => {
    const on_click_818f1c5c61d84492101c741bb804ca3a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "torch" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_818f1c5c61d84492101c741bb804ca3a }))},children)
    )
});
Button_button_b5575478594af6ab2cd906a710cdfbe4_cfd3635a.displayName = "Button";
return Button_button_b5575478594af6ab2cd906a710cdfbe4_cfd3635a;
})();

export const Button_button_a69ae905019e323c127ca23066d87e7c_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_a69ae905019e323c127ca23066d87e7c_cfd3635a = memo(({children, ...rest}) => {
    const on_click_5bec0f8897a5068ce9a32a24a1035a2b = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "tensorflow" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_5bec0f8897a5068ce9a32a24a1035a2b }))},children)
    )
});
Button_button_a69ae905019e323c127ca23066d87e7c_cfd3635a.displayName = "Button";
return Button_button_a69ae905019e323c127ca23066d87e7c_cfd3635a;
})();

export const Bare_comp_5ab6f538659d533714715a63cb92d666_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_5ab6f538659d533714715a63cb92d666_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.initials_rx_state_
    )
});
Bare_comp_5ab6f538659d533714715a63cb92d666_cfd3635a.displayName = "Bare";
return Bare_comp_5ab6f538659d533714715a63cb92d666_cfd3635a;
})();

export const Box_box_c22865b79f321cbc36a1b8dbd5f84564_cfd3635a = /*#__PURE__*/ (() => {
const Box_box_c22865b79f321cbc36a1b8dbd5f84564_cfd3635a = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(RadixThemesBox,{...mergeSlotProps(rest, ({ css:({ ["background"] : reflex___state____state__reflexsqlite___state___base____auth_state.avatar_color_rx_state_, ["borderRadius"] : "999px", ["width"] : "32px", ["height"] : "32px", ["minWidth"] : "32px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" }) }))},children)
    )
});
Box_box_c22865b79f321cbc36a1b8dbd5f84564_cfd3635a.displayName = "Box";
return Box_box_c22865b79f321cbc36a1b8dbd5f84564_cfd3635a;
})();

export const Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.display_name_rx_state_
    )
});
Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_cfd3635a.displayName = "Bare";
return Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_cfd3635a;
})();

export const Bare_comp_bcff288a0ef24fc2c402098247cbd23b_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_bcff288a0ef24fc2c402098247cbd23b_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.role_rx_state_
    )
});
Bare_comp_bcff288a0ef24fc2c402098247cbd23b_cfd3635a.displayName = "Bare";
return Bare_comp_bcff288a0ef24fc2c402098247cbd23b_cfd3635a;
})();

export const Button_button_f9de5aac8983a4287e20b52d3112c0ce_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_f9de5aac8983a4287e20b52d3112c0ce_cfd3635a = memo(({children, ...rest}) => {
    const on_click_42b68d07de6d2f872f818321f5b24e9f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.sign_out", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_42b68d07de6d2f872f818321f5b24e9f }))},children)
    )
});
Button_button_f9de5aac8983a4287e20b52d3112c0ce_cfd3635a.displayName = "Button";
return Button_button_f9de5aac8983a4287e20b52d3112c0ce_cfd3635a;
})();

export const Box_box_c278a0e4c5a8808b61724d3b452c28ba_cfd3635a = /*#__PURE__*/ (() => {
const Box_box_c278a0e4c5a8808b61724d3b452c28ba_cfd3635a = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        jsx(RadixThemesBox,{...mergeSlotProps(rest, ({ css:({ ["background"] : reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.active_library_color_rx_state_, ["borderRadius"] : "12px", ["width"] : "46px", ["height"] : "46px", ["minWidth"] : "46px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" }) }))},children)
    )
});
Box_box_c278a0e4c5a8808b61724d3b452c28ba_cfd3635a.displayName = "Box";
return Box_box_c278a0e4c5a8808b61724d3b452c28ba_cfd3635a;
})();

export const Bare_comp_b0411075989be1c4e655a4aca08b731e_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_b0411075989be1c4e655a4aca08b731e_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.active_library_name_rx_state_
    )
});
Bare_comp_b0411075989be1c4e655a4aca08b731e_cfd3635a.displayName = "Bare";
return Bare_comp_b0411075989be1c4e655a4aca08b731e_cfd3635a;
})();

export const Bare_comp_dd75691db3307976fa5f5134be2efdac_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_dd75691db3307976fa5f5134be2efdac_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.library_version_rx_state_
    )
});
Bare_comp_dd75691db3307976fa5f5134be2efdac_cfd3635a.displayName = "Bare";
return Bare_comp_dd75691db3307976fa5f5134be2efdac_cfd3635a;
})();

export const Bare_comp_c92c1ae21c16dd4fdc49c2ea7d6de46e_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_c92c1ae21c16dd4fdc49c2ea7d6de46e_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.active_op_description_rx_state_
    )
});
Bare_comp_c92c1ae21c16dd4fdc49c2ea7d6de46e_cfd3635a.displayName = "Bare";
return Bare_comp_c92c1ae21c16dd4fdc49c2ea7d6de46e_cfd3635a;
})();

export const Cond_comp_3b73786b6a902accc201393163098493_cfd3635a = /*#__PURE__*/ (() => {
const Cond_comp_3b73786b6a902accc201393163098493_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        (reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.library_available_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3b73786b6a902accc201393163098493_cfd3635a.displayName = "Cond";
return Cond_comp_3b73786b6a902accc201393163098493_cfd3635a;
})();

export const Foreach_comp_7e7a5f94ad25b52c246f29ff96919f47_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_7e7a5f94ad25b52c246f29ff96919f47_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.operations_rx_state_ ?? [],((op_rx_state_,index_d63319cab7646edb3d6ec91c9259a336)=>(jsx(RadixThemesButton,{css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "10px", ["padding"] : "11px 13px", ["width"] : "100%", ["cursor"] : "pointer", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #C7D2FE" }) }),key:index_d63319cab7646edb3d6ec91c9259a336,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.select_operation", ({ ["operation_id"] : op_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "3px", ["alignItems"] : "start", ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "12px", ["fontWeight"] : "650", ["color"] : "#111827" })},op_rx_state_?.["label"]),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B", ["textAlign"] : "left", ["lineHeight"] : "1.4" })},op_rx_state_?.["description"]))))))
    )
});
Foreach_comp_7e7a5f94ad25b52c246f29ff96919f47_cfd3635a.displayName = "Foreach";
return Foreach_comp_7e7a5f94ad25b52c246f29ff96919f47_cfd3635a;
})();

export const Foreach_comp_4f99b02091bd12278d2d45eede250625_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_4f99b02091bd12278d2d45eede250625_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.datasets_rx_state_ ?? [],((item_rx_state_,index_95d0bbc884f4a5dbfca310b9c56280d2)=>(jsx(RadixThemesButton,{css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "8px", ["padding"] : "7px 11px", ["cursor"] : "pointer" }),key:index_95d0bbc884f4a5dbfca310b9c56280d2,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.select_dataset", ({ ["dataset_id"] : item_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["fontWeight"] : "600", ["color"] : "#111827" })},item_rx_state_?.["name"])))))
    )
});
Foreach_comp_4f99b02091bd12278d2d45eede250625_cfd3635a.displayName = "Foreach";
return Foreach_comp_4f99b02091bd12278d2d45eede250625_cfd3635a;
})();

export const Foreach_comp_54500a80d0526556a86106a7802f494d_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_54500a80d0526556a86106a7802f494d_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.x_options_rx_state_ ?? [],((item_rx_state_,index_a4c056de887ac0859af139cad1744de9)=>(jsx(RadixThemesSelect.Item,{key:index_a4c056de887ac0859af139cad1744de9,value:item_rx_state_},item_rx_state_))))
    )
});
Foreach_comp_54500a80d0526556a86106a7802f494d_cfd3635a.displayName = "Foreach";
return Foreach_comp_54500a80d0526556a86106a7802f494d_cfd3635a;
})();

export const Selectroot_select__root_f94b62ff42d3eab32b234084f197bd4e_cfd3635a = /*#__PURE__*/ (() => {
const Selectroot_select__root_f94b62ff42d3eab32b234084f197bd4e_cfd3635a = memo(({children, ...rest}) => {
    const on_change_27bc74713984304bb1cc30e41a34bdd5 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.set_x_column", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        jsx(RadixThemesSelect.Root,{...mergeSlotProps(rest, ({ onValueChange:on_change_27bc74713984304bb1cc30e41a34bdd5, size:"1", value:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.x_column_rx_state_ }))},children)
    )
});
Selectroot_select__root_f94b62ff42d3eab32b234084f197bd4e_cfd3635a.displayName = "SelectRoot";
return Selectroot_select__root_f94b62ff42d3eab32b234084f197bd4e_cfd3635a;
})();

export const Foreach_comp_ed7b5765e4073c44e84dbab891a36e47_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_ed7b5765e4073c44e84dbab891a36e47_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.y_options_rx_state_ ?? [],((item_rx_state_,index_a4c056de887ac0859af139cad1744de9)=>(jsx(RadixThemesSelect.Item,{key:index_a4c056de887ac0859af139cad1744de9,value:item_rx_state_},item_rx_state_))))
    )
});
Foreach_comp_ed7b5765e4073c44e84dbab891a36e47_cfd3635a.displayName = "Foreach";
return Foreach_comp_ed7b5765e4073c44e84dbab891a36e47_cfd3635a;
})();

export const Selectroot_select__root_1e8de346bf2977064fcfe76a46db1d9c_cfd3635a = /*#__PURE__*/ (() => {
const Selectroot_select__root_1e8de346bf2977064fcfe76a46db1d9c_cfd3635a = memo(({children, ...rest}) => {
    const on_change_3b7df55c9c9f20d9c14327c1dcdd417f = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.set_y_column", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        jsx(RadixThemesSelect.Root,{...mergeSlotProps(rest, ({ onValueChange:on_change_3b7df55c9c9f20d9c14327c1dcdd417f, size:"1", value:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.y_column_rx_state_ }))},children)
    )
});
Selectroot_select__root_1e8de346bf2977064fcfe76a46db1d9c_cfd3635a.displayName = "SelectRoot";
return Selectroot_select__root_1e8de346bf2977064fcfe76a46db1d9c_cfd3635a;
})();

export const Button_button_59b3229080a225078ea84ac8bb0ca0d1_cfd3635a = /*#__PURE__*/ (() => {
const Button_button_59b3229080a225078ea84ac8bb0ca0d1_cfd3635a = memo(({children, ...rest}) => {
    const on_click_0bc26d87bba68ab217ba4c7dc44db647 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.run_analysis", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }), ["marginTop"] : "14px" }), disabled:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.is_running_rx_state_, onClick:on_click_0bc26d87bba68ab217ba4c7dc44db647 }))},children)
    )
});
Button_button_59b3229080a225078ea84ac8bb0ca0d1_cfd3635a.displayName = "Button";
return Button_button_59b3229080a225078ea84ac8bb0ca0d1_cfd3635a;
})();

export const Bare_comp_31a5a6b98c8239ed2bad35d4d032ef9f_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_31a5a6b98c8239ed2bad35d4d032ef9f_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.explore_error_rx_state_
    )
});
Bare_comp_31a5a6b98c8239ed2bad35d4d032ef9f_cfd3635a.displayName = "Bare";
return Bare_comp_31a5a6b98c8239ed2bad35d4d032ef9f_cfd3635a;
})();

export const Cond_comp_2bafc4716ad29dbfe5b8fdbd1b756ddf_cfd3635a = /*#__PURE__*/ (() => {
const Cond_comp_2bafc4716ad29dbfe5b8fdbd1b756ddf_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.explore_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_2bafc4716ad29dbfe5b8fdbd1b756ddf_cfd3635a.displayName = "Cond";
return Cond_comp_2bafc4716ad29dbfe5b8fdbd1b756ddf_cfd3635a;
})();

export const Bare_comp_6bea507a1b4104d3e10010a94d175da7_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_6bea507a1b4104d3e10010a94d175da7_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_summary_rx_state_
    )
});
Bare_comp_6bea507a1b4104d3e10010a94d175da7_cfd3635a.displayName = "Bare";
return Bare_comp_6bea507a1b4104d3e10010a94d175da7_cfd3635a;
})();

export const Bare_comp_2a086e7ad5c063d7a44b0a17c44d51e7_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_2a086e7ad5c063d7a44b0a17c44d51e7_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_library_rx_state_
    )
});
Bare_comp_2a086e7ad5c063d7a44b0a17c44d51e7_cfd3635a.displayName = "Bare";
return Bare_comp_2a086e7ad5c063d7a44b0a17c44d51e7_cfd3635a;
})();

export const Bare_comp_effe78ae8f121ca506241303c0dc1b66_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_effe78ae8f121ca506241303c0dc1b66_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_title_rx_state_
    )
});
Bare_comp_effe78ae8f121ca506241303c0dc1b66_cfd3635a.displayName = "Bare";
return Bare_comp_effe78ae8f121ca506241303c0dc1b66_cfd3635a;
})();

export const Foreach_comp_e500143277eb9debcc2c06b29ac14950_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_e500143277eb9debcc2c06b29ac14950_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_metrics_rx_state_ ?? [],((item_rx_state_,index_425a9af846bdc0b1e5d5d3391702b32e)=>(jsx(RadixThemesBox,{css:({ ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "14px", ["boxShadow"] : "0 1px 2px rgba(16,24,40,.04), 0 8px 24px rgba(16,24,40,.05)", ["padding"] : "14px", ["minWidth"] : "130px" }),key:index_425a9af846bdc0b1e5d5d3391702b32e},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "3px", ["alignItems"] : "start" }),direction:"column",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B", ["fontWeight"] : "600" })},item_rx_state_?.["label"]),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "18px", ["fontWeight"] : "750", ["color"] : "#111827" })},item_rx_state_?.["value"]),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "9px", ["color"] : "#94A3B8" })},item_rx_state_?.["hint"]))))))
    )
});
Foreach_comp_e500143277eb9debcc2c06b29ac14950_cfd3635a.displayName = "Foreach";
return Foreach_comp_e500143277eb9debcc2c06b29ac14950_cfd3635a;
})();

export const Img_img_524e27cd571117bf13d2c219e17a37e1_cfd3635a = /*#__PURE__*/ (() => {
const Img_img_524e27cd571117bf13d2c219e17a37e1_cfd3635a = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:"Library figure", css:({ ["width"] : "100%", ["borderRadius"] : "10px" }), src:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_image_rx_state_ }))},)
    )
});
Img_img_524e27cd571117bf13d2c219e17a37e1_cfd3635a.displayName = "Img";
return Img_img_524e27cd571117bf13d2c219e17a37e1_cfd3635a;
})();

export const Cond_comp_2aa0a4f60f0bf3c37d0961149660129d_cfd3635a = /*#__PURE__*/ (() => {
const Cond_comp_2aa0a4f60f0bf3c37d0961149660129d_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_image_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_2aa0a4f60f0bf3c37d0961149660129d_cfd3635a.displayName = "Cond";
return Cond_comp_2aa0a4f60f0bf3c37d0961149660129d_cfd3635a;
})();

export const Responsivecontainer_responsivecontainer_eaf051f3b41ed8a093562abf72cdcc56_cfd3635a = /*#__PURE__*/ (() => {
const Responsivecontainer_responsivecontainer_eaf051f3b41ed8a093562abf72cdcc56_cfd3635a = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        jsx(RechartsResponsiveContainer,{...mergeSlotProps(rest, ({ height:260, minHeight:10, minWidth:10, width:"100%" }))},jsx(RechartsComposedChart,{data:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_chart_rx_state_,height:"100%",margin:({ ["top"] : 10, ["right"] : 16, ["left"] : 4, ["bottom"] : 6 }),width:"100%"},jsx(RechartsCartesianGrid,{stroke:"#EEF1F7",strokeDasharray:"3 3",vertical:false},),jsx(RechartsXAxis,{axisLine:false,dataKey:"name",height:28,stroke:"var(--gray-9)",tickLine:false},),jsx(RechartsYAxis,{axisLine:false,stroke:"var(--gray-9)",tickLine:false,width:52},),jsx(RechartsTooltip,{contentStyle:({ ["fontSize"] : "11px", ["borderRadius"] : "8px" }),cursor:({ ["strokeWidth"] : 1, ["fill"] : "var(--gray-3)" }),itemStyle:({ ["color"] : "var(--gray-12)" }),labelStyle:({ ["color"] : "var(--gray-11)" })},),jsx(RechartsBar,{dataKey:"value",fill:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_color_rx_state_,isAnimationActive:false,name:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_chart_label_rx_state_,radius:[4, 4, 0, 0]},),jsx(Fragment,{},(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_secondary_rx_state_?(jsx(Fragment,{},jsx(RechartsLine,{activeDot:({ ["stroke"] : "var(--accent-2)", ["fill"] : "var(--accent-10)" }),dataKey:"extra",dot:false,isAnimationActive:false,name:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_secondary_label_rx_state_,stroke:"#0EA5E9",strokeWidth:2},))):(jsx(Fragment,{},))))))
    )
});
Responsivecontainer_responsivecontainer_eaf051f3b41ed8a093562abf72cdcc56_cfd3635a.displayName = "ResponsiveContainer";
return Responsivecontainer_responsivecontainer_eaf051f3b41ed8a093562abf72cdcc56_cfd3635a;
})();

export const Cond_comp_98f96984330bc3f0bd0010ffa51e83c3_cfd3635a = /*#__PURE__*/ (() => {
const Cond_comp_98f96984330bc3f0bd0010ffa51e83c3_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        (reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.has_result_chart_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_98f96984330bc3f0bd0010ffa51e83c3_cfd3635a.displayName = "Cond";
return Cond_comp_98f96984330bc3f0bd0010ffa51e83c3_cfd3635a;
})();

export const Foreach_comp_b16d52b784b2ec802fa56a57954a1cc6_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_b16d52b784b2ec802fa56a57954a1cc6_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_table_columns_rx_state_ ?? [],((col_rx_state_,index_fb0574821ac14a94164c40ce54e03fa9)=>(jsx(RadixThemesBox,{css:({ ["minWidth"] : "110px", ["flex"] : "1", ["padding"] : "9px 8px" }),key:index_fb0574821ac14a94164c40ce54e03fa9},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["fontWeight"] : "700", ["color"] : "#64748B", ["whiteSpace"] : "nowrap" })},col_rx_state_)))))
    )
});
Foreach_comp_b16d52b784b2ec802fa56a57954a1cc6_cfd3635a.displayName = "Foreach";
return Foreach_comp_b16d52b784b2ec802fa56a57954a1cc6_cfd3635a;
})();

export const Foreach_comp_8b11afd3c2bfdf8e4544a40650687b72_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_8b11afd3c2bfdf8e4544a40650687b72_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_table_rows_rx_state_ ?? [],((row_rx_state_,index_f455de09583673f2f3dd9911d4920dd9)=>(jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["borderBottom"] : "1px solid #E5E8F1", ["gap"] : "0", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }),direction:"row",key:index_f455de09583673f2f3dd9911d4920dd9,gap:"3"},Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_table_columns_rx_state_ ?? [],((col_rx_state_,index_ed32ac638a876b8e70d666686dfcdef9)=>(jsx(RadixThemesBox,{css:({ ["minWidth"] : "110px", ["flex"] : "1", ["padding"] : "8px", ["overflow"] : "hidden" }),key:index_ed32ac638a876b8e70d666686dfcdef9},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["color"] : "#111827", ["whiteSpace"] : "nowrap" })},row_rx_state_?.[col_rx_state_])))))))))
    )
});
Foreach_comp_8b11afd3c2bfdf8e4544a40650687b72_cfd3635a.displayName = "Foreach";
return Foreach_comp_8b11afd3c2bfdf8e4544a40650687b72_cfd3635a;
})();

export const Foreach_comp_a7c14076be467ce813eba8d1db41c0ee_cfd3635a = /*#__PURE__*/ (() => {
const Foreach_comp_a7c14076be467ce813eba8d1db41c0ee_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_notes_rx_state_ ?? [],((note_rx_state_,index_d2364ed62d0658eb63e03c0b5b593ca6)=>(jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B" }),key:index_d2364ed62d0658eb63e03c0b5b593ca6},note_rx_state_))))
    )
});
Foreach_comp_a7c14076be467ce813eba8d1db41c0ee_cfd3635a.displayName = "Foreach";
return Foreach_comp_a7c14076be467ce813eba8d1db41c0ee_cfd3635a;
})();

export const Bare_comp_f9d3aba6ae5c89e1c7e5ac50c6c688ba_cfd3635a = /*#__PURE__*/ (() => {
const Bare_comp_f9d3aba6ae5c89e1c7e5ac50c6c688ba_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.result_elapsed_label_rx_state_
    )
});
Bare_comp_f9d3aba6ae5c89e1c7e5ac50c6c688ba_cfd3635a.displayName = "Bare";
return Bare_comp_f9d3aba6ae5c89e1c7e5ac50c6c688ba_cfd3635a;
})();

export const Cond_comp_405dd6ba00c68bfab9ed1e84c660ab1b_cfd3635a = /*#__PURE__*/ (() => {
const Cond_comp_405dd6ba00c68bfab9ed1e84c660ab1b_cfd3635a = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state")
    return(
        (reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___explore_state____explore_state.has_result_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_405dd6ba00c68bfab9ed1e84c660ab1b_cfd3635a.displayName = "Cond";
return Cond_comp_405dd6ba00c68bfab9ed1e84c660ab1b_cfd3635a;
})();

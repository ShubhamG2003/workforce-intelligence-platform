ATTENDANCE_QUERY = """
SELECT
    date,
    employeeid,
    shiftname,
    summaryworkedhours,
    latein,
    totalbreaktime,
    numberofbreaks,
    exceptiontype
FROM workforce_attendance
"""